from fastapi import Header
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.orm import Session
from contextlib import contextmanager
import time
import json
import socket
from app.core.logging_config import logger
from datetime import datetime
from fastapi import Request, HTTPException
from sqlalchemy.exc import OperationalError

from app.core.config import DB_CONFIGS as CLUSTERS
from app.utils.mg_broker import send_message_to_rabbitmq
from app.core.config import DB_CONFIGS, settings
import traceback
import re

def ensure_str(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)

# Database URL
def get_engine(db_server_name: str, db_name: str):
    try:
        if settings.APP_ENV == "dev":
            db_server_name = "dev"

        db_config = DB_CONFIGS[db_server_name]
        user = ensure_str(db_config.get("DB_USER"))
        password = ensure_str(db_config.get("DB_PASSWORD"))
        host = ensure_str(db_config.get("DB_HOST"))
        port = ensure_str(db_config.get("DB_PORT"))
        try:
            user = urllib.parse.quote(user)
            password = urllib.parse.quote(password)
            host = urllib.parse.quote(host)
            DATABASE_URL = (f"mysql://{user}:{password}@{host}:{port}/{db_name}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Invalid DB URL build: {e}")
        
        try:
            engine = create_engine(DATABASE_URL, echo=False)
        except OperationalError as e:
            raise HTTPException(status_code=503, detail=f"Database connection failed: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Engine creation failed: {e} ")


    except Exception as e:
        print(f"Could not connect to database: {e}")
        raise


    # Event listeners for query logging
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        try:
            conn.info["query_start_time"] = time.time()
        except Exception as e:
            logger.warning(f"before_cursor_execute failed: {e}")

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        try:
            start_time = conn.info.get("query_start_time")
            if start_time is not None:
                execution_time = time.time() - start_time
                execution_options = context.connection._execution_options
                headers = execution_options.get("headers", {})
                cluster_name = execution_options.get("cluster_name", "unknown")
                db_name = execution_options.get("db_name", "unknown")

                cluster_config = CLUSTERS.get(cluster_name, {})
                db_config = cluster_config.get(db_name, {})
            
                if headers:
                    sys_key = headers.get("SYS-KEY", "unknown")
                    person_id = headers.get("PERSON-ID", "unknown")
                    user_roles = headers.get("USER-ROLES", "unknown")
                    ip_address = headers.get("IP-ADDRESS", "unknown")
                    user_id = headers.get("USER-ID", "unknown")
                    user_roles = headers.get("USER-ROLES","unknown")

                else:
                    sys_key = person_id = user_roles = ip_address = user_id = "unknown"

                try:
                    safe_params = json.dumps(parameters, default=_json_default, ensure_ascii=False)
                except Exception:

                    try:
                        safe_params = json.dumps(list(parameters), default=_json_default, ensure_ascii=False)
                    except Exception:
                        safe_params = str(parameters)

                log = {
                    "executemany": executemany,
                    "query": str(statement),
                    "SerializedParam": safe_params,
                    "UserID": user_id,  # Use USER-ID from headers
                    "IPAddress": ip_address,  # Use IP-ADDRESS from headers
                    "SysCode": sys_key,  # Use SYS-KEY from headers
                    "PersonID": person_id,  # Use PERSON-ID from headers
                    "UserRoles": user_roles,  # Use USER-ROLES from headers
                    "ExecuteTime": round(execution_time,8),
                    "QueryStatus": "successful",
                    "DBName": db_config.get("DB_NAME", "unknown"),
                    "DBUser": db_config.get("DB_USER", "unknown"),
                    "DBHost": int.from_bytes(socket.inet_aton(socket.gethostbyname(cluster_config.get("DB_HOST", "localhost"))), byteorder="big"),
                    "DBClass": "SqlAlchemy",
                    "ATSLog": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                send_message_to_rabbitmq(json.dumps(log))
                if settings.APP_ENV == "dev":
                    print(log)
        except Exception as e:
            logger.warning(f"after_cursor_execute failed: {e}")

    @event.listens_for(engine, "handle_error")
    def handle_error(exception_context):
        try:
            execution_options = exception_context.connection._execution_options
            headers = execution_options.get("headers", {})
            cluster_name = execution_options.get("cluster_name", "unknown")
            db_name = execution_options.get("db_name", "unknown")

            cluster_config = CLUSTERS.get(cluster_name, {})
            db_config = cluster_config.get(db_name, {})

            if headers:
                sys_key = headers.get("SYS-KEY", "unknown")
                person_id = headers.get("PERSON-ID", "unknown")
                user_roles = headers.get("USER-ROLES", "unknown")
                ip_address = headers.get("IP-ADDRESS", "unknown")
                user_id = headers.get("USER-ID", "unknown")
                user_roles = headers.get("USER-ROLES","unknown")
            else:
                sys_key = person_id = user_roles = ip_address = user_id = "unknown"

            log = {
                "query": str(exception_context.statement),
                "SerializedParam": json.dumps(exception_context.parameters),
                "exception": str(exception_context.original_exception),
                "IPAddress": ip_address,  # Use IP-ADDRESS from headers
                "SysCode": sys_key,  # Use SYS-KEY from headers
                "PersonID": person_id,  # Use PERSON-ID from headers
                "UserRoles": user_roles,  # Use USER-ROLES from headers
                "UserID": user_id,  # Use USER-ID from headers
                "QueryStatus": "failed",
                "DBName": db_config.get("DB_NAME", "unknown"),
                "DBUser": db_config.get("DB_USER", "unknown"),
                "DBHost": int.from_bytes(socket.inet_aton(socket.gethostbyname(cluster_config.get("DB_HOST", "localhost"))), byteorder="big"),
                "DBClass": "SqlAlchemy",
                "ATSLog": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            send_message_to_rabbitmq(json.dumps(log))
            logger.error("Query Failed: %s", exception_context.statement, extra=log)
        except Exception as e:
            logger.warning(f"handle_error logging failed: {e}")        
    return engine



def get_session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

def extract_real_db_error(e: Exception) -> str:
    """
    تلاش برای بیرون کشیدن پیام خطای واقعی MySQL از exception chain.
    """
    # اگر SQLAlchemy یک خطای دیتابیسی استاندارد است
    if hasattr(e, "orig") and e.orig:
        return str(e.orig)

    # اگر cause یا context دارد (exception chain)
    cause = getattr(e, "__cause__", None) or getattr(e, "__context__", None)
    if cause:
        return extract_real_db_error(cause)

    # اگر traceback شامل MySQL error هست
    tb = traceback.format_exc()
    mysql_msg = re.search(r"Access denied for user.+", tb)
    if mysql_msg:
        return mysql_msg.group(0)

    return str(e)

# Database session dependency
@contextmanager
def get_session(request: Request, db_server_name: str, db_name: str):
    engine = get_engine(db_server_name, db_name)  # Get the engine for the specified cluster and database
    SessionLocal = get_session_factory(engine)  # Create a session factory
    db = SessionLocal()  # Create a session
    try:
        headers = {
        "SYS-KEY": request.headers.get("SYS-KEY", request.client.host),
        "PERSON-ID": request.headers.get("PERSON-ID", request.client.host),
        "IP-ADDRESS": request.headers.get("IP-ADDRESS", request.client.host),
        "USER-ID": request.headers.get("USER-ID", request.client.host),
        "USER-ROLES": request.headers.get("USER-ROLES", request.client.host)

        }
        try:
            db.connection(execution_options={ "headers": headers, "cluster_name": db_server_name, "db_name": db_name})
        except OperationalError as e:
            orig_msg = str(getattr(e, "orig", e))
            raise HTTPException(
                status_code=503,
                detail=f"Database connection failed: {orig_msg}"
            )
        except Exception as e:
            msg = extract_real_db_error(e)
            #full_tb = traceback.format_exc()
            orig_msg = str(getattr(e, "orig", e))
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected database error: {msg}",
                #headers={"X-Trace": full_tb}  
            )

        yield db
    finally:
        db.close()

def get_db(request: Request, db_server_name: str, db_name: str ) -> Session:
    with get_session(request, db_server_name, db_name) as session:
        yield session

def get_db_officedb(request: Request):
    yield from get_db(request, "officedb", "projectmanagement")

def get_db_masterdb(request: Request):
    yield from get_db(request, "master", "framework")

