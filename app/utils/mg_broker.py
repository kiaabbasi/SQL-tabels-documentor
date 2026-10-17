import json
import logging
import time

from app.core.config import settings

logger = logging.getLogger("app.mg_broker")

# Opt-in RabbitMQ config from env; no-op when not configured.
RABBITMQ_URL: str | None = getattr(settings, "RABBITMQ_URL", None)
RABBITMQ_HOST: str | None = getattr(settings, "RABBITMQ_HOST", None)
RABBITMQ_PORT: int = int(settings.RABBITMQ_PORT)
RABBITMQ_QUEUE: str = settings.RABBITMQ_QUEUE

_connection = None
_channel = None
_last_failure: float = 0.0
_FAILURE_COOLDOWN_SECONDS: float = 30.0  # don't retry a dead broker on every log


def _get_channel():
    """Return a cached pika channel, reconnecting if needed."""
    global _connection, _channel

    import pika

    if _channel is not None and _channel.is_open:
        return _channel

    try:
        if _connection is not None and _connection.is_open:
            _connection.close()
    except Exception:
        pass

    if RABBITMQ_URL:
        _connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    else:
        _connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
    _channel = _connection.channel()
    _channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    return _channel


def send_message_to_rabbitmq(message: str | dict) -> None:
    """
    Publish a message to RabbitMQ.

    Never raises: query auditing is best-effort and must not break API requests.
    No-op when no RabbitMQ config is available.
    """
    if not (RABBITMQ_URL or RABBITMQ_HOST):
        return

    global _last_failure
    if time.monotonic() - _last_failure < _FAILURE_COOLDOWN_SECONDS:
        return  # broker just failed; skip this log entry

    try:
        channel = _get_channel()
        if isinstance(message, (dict, list)):
            message = json.dumps(message, ensure_ascii=False)
        channel.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=message.encode("utf-8"),
            properties=None,
            mandatory=False,
        )
    except Exception as e:
        # Broken broker must never break the request path.
        _last_failure = time.monotonic()
        logger.warning("send_message_to_rabbitmq failed: %s", e)
