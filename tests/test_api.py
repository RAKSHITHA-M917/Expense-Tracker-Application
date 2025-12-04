import os
import tempfile
import pytest
from app import create_app
from db import db as _db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    test_config = {"SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}", "TESTING": True}
    app = create_app()
    app.config.update(test_config)
    with app.app_context():
        _db.create_all()
    yield app
    os.close(db_fd)
    os.remove(db_path)

def test_budget_and_expense(client, app):
    rv = client.post("/api/budget", json={"category":"Food","month":"2025-12","amount":100.0})
    assert rv.status_code == 200

    rv = client.post("/api/expense", json={"title":"Lunch","category":"Food","amount":30.0,"date":"2025-12-01"})
    assert rv.status_code == 201

    rv = client.get("/api/report/monthly?month=2025-12")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["total"] == 30.0

    rv = client.get("/api/report/compare?month=2025-12")
    assert rv.status_code == 200
    comp = rv.get_json()
    assert comp["comparisons"]["Food"]["spent"] == 30.0