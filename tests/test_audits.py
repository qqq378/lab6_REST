import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import audit_store


@pytest.fixture(autouse=True)
def clean_store():
    audit_store.clear()
    yield
    audit_store.clear()


client = TestClient(app)


def _payload():
    return {
        "audit_number": "A-2025-01",
        "department": "Локомотивное депо Гомель",
        "scope": "Процесс технического обслуживания",
        "criteria": "ISO 9001:2015, п. 9.2",
        "planned_date": "2025-03-15",
        "status": "planned",
        "lead_auditor": "Иванов И.И.",
        "auditors": ["Петров П.П.", "Сидоров С.С."],
    }


def test_list_empty():
    r = client.get("/api/v1/audits/")
    assert r.status_code == 200
    assert r.json() == []


def test_create_and_get():
    r = client.post("/api/v1/audits/", json=_payload())
    assert r.status_code == 201
    audit_id = r.json()["id"]

    r = client.get(f"/api/v1/audits/{audit_id}")
    assert r.status_code == 200
    assert r.json()["audit_number"] == "A-2025-01"


def test_get_not_found():
    r = client.get("/api/v1/audits/999")
    assert r.status_code == 404


def test_delete():
    r = client.post("/api/v1/audits/", json=_payload())
    audit_id = r.json()["id"]
    r = client.delete(f"/api/v1/audits/{audit_id}")
    assert r.status_code == 204
    r = client.get(f"/api/v1/audits/{audit_id}")
    assert r.status_code == 404


def test_delete_not_found():
    r = client.delete("/api/v1/audits/999")
    assert r.status_code == 404


def test_create_invalid():
    bad = _payload()
    bad["audit_number"] = ""
    r = client.post("/api/v1/audits/", json=bad)
    assert r.status_code == 422