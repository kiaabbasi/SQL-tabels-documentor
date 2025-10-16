import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.services import epic_service
from db.schemas.epic import EpicCreate, EpicUpdate


# -------------------------
# Unit Tests (service layer)
# -------------------------

@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_create_epic_unit(db_session: Session, sample_person_id1, sample_product_id):
    epic_in = EpicCreate(
        title="Epic 1",
        description="Epic description"
    )
    epic = epic_service.create_epic(db_session, sample_product_id, epic_in, sample_person_id1)
    assert epic.EpicID is not None
    assert epic.title == "Epic 1"
    assert epic.ProductID == sample_product_id


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_get_epic_unit(db_session: Session, sample_person_id1, sample_product_id):
    epic_in = EpicCreate(title="Epic 2", description="Test desc")
    epic = epic_service.create_epic(db_session, sample_product_id, epic_in, sample_person_id1)

    fetched = epic_service.get_epic(db_session, epic.EpicID)
    assert fetched is not None
    assert fetched.EpicID == epic.EpicID
    assert fetched.title == "Epic 2"


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_update_epic_unit(db_session: Session, sample_person_id1, sample_product_id):
    epic_in = EpicCreate(title="Old Epic", description="Old desc")
    epic = epic_service.create_epic(db_session, sample_product_id, epic_in, sample_person_id1)

    update_in = EpicUpdate(title="New Epic", description="New desc")
    updated = epic_service.update_epic(db_session, epic.EpicID, update_in)
    assert updated.title == "New Epic"
    assert updated.description == "New desc"


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_delete_epic_unit(db_session: Session, sample_person_id1, sample_product_id):
    epic_in = EpicCreate(title="ToDelete", description="Del me")
    epic = epic_service.create_epic(db_session, sample_product_id, epic_in, sample_person_id1)

    deleted = epic_service.delete_epic(db_session, epic.EpicID)
    assert deleted is not None
    assert deleted.EpicID == epic.EpicID
    assert epic_service.get_epic(db_session, epic.EpicID) is None


# ----------------------------
# Integration Tests (endpoints)
# ----------------------------

@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_create_epic_integration(client: TestClient, sample_person_id1, sample_product_id):
    data = {"title": "API Epic", "description": "Created via API"}
    headers = {"PERSON-ID": str(sample_person_id1)}
    response = client.post(f"/api/v1/products/{sample_product_id}/epics/", json=data, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "API Epic"
    assert "EpicID" in body


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_list_epics_integration(client: TestClient, sample_product_id):
    response = client.get(f"/api/v1/products/{sample_product_id}/epics/")
    assert response.status_code in (200, 404)


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_update_epic_integration_authorized(client: TestClient, sample_person_id1, sample_product_id):
    headers = {"PERSON-ID": str(sample_person_id1)}
    res = client.post(
        f"/api/v1/products/{sample_product_id}/epics/",
        json={"title": "Old Epic", "description": ""},
        headers=headers
    )
    epic_id = res.json()["EpicID"]

    response = client.put(
        f"/api/v1/products/{sample_product_id}/epics/{epic_id}",
        json={"title": "New Epic"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Epic"


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_update_epic_integration_unauthorized(client: TestClient, sample_person_id1, sample_person_id2, sample_product_id):
    headers = {"PERSON-ID": str(sample_person_id1)}
    res = client.post(
        f"/api/v1/products/{sample_product_id}/epics/",
        json={"title": "Epic U", "description": "unauthorized"},
        headers=headers
    )
    epic_id = res.json()["EpicID"]

    headers = {"PERSON-ID": str(sample_person_id2)}
    response = client.put(
        f"/api/v1/products/{sample_product_id}/epics/{epic_id}",
        json={"title": "Hack"},
        headers=headers
    )
    assert response.status_code == 403


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_delete_epic_integration_authorized(client: TestClient, sample_person_id1, sample_product_id):
    headers = {"PERSON-ID": str(sample_person_id1)}
    res = client.post(
        f"/api/v1/products/{sample_product_id}/epics/",
        json={"title": "Del Epic", "description": "Remove me"},
        headers=headers
    )
    epic_id = res.json()["EpicID"]

    response = client.delete(f"/api/v1/products/{sample_product_id}/epics/{epic_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "epic removed successfully"


@pytest.mark.usefixtures("clean_epics", "clean_products")
def test_delete_epic_integration_unauthorized(client: TestClient, sample_person_id1, sample_person_id2, sample_product_id):
    headers = {"PERSON-ID": str(sample_person_id1)}
    res = client.post(
        f"/api/v1/products/{sample_product_id}/epics/",
        json={"title": "Del Epic2", "description": ""},
        headers=headers
    )
    epic_id = res.json()["EpicID"]

    headers = {"PERSON-ID": str(sample_person_id2)}
    response = client.delete(f"/api/v1/products/{sample_product_id}/epics/{epic_id}", headers=headers)
    assert response.status_code == 403
