import pytest
from flask import url_for, request

import server


def test_dashboard_acces_ok(client, clubs_mocked_data):
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert request.path == url_for("dashboard")


def test_dashboard_data_ok(client, clubs_mocked_data):
    response = client.get("/dashboard")
    club1 = clubs_mocked_data[0]
    club2 = clubs_mocked_data[1]

    assert club1["name"] in response.data.decode()
    assert club1["points"] in response.data.decode()
    assert club2["name"] in response.data.decode()
    assert club2["points"] in response.data.decode()
