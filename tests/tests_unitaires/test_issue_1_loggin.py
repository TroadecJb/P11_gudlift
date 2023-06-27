from flask import url_for, request


def test_page_index_status_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_status_ok(client, clubs_mocked_data):
    response = client.post(
        "/showSummary",
        data=dict(email=clubs_mocked_data[0]["email"]),
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_login_status_invalid_email(client, club_invalid, clubs_mocked_data):
    response = client.post(
        "/showSummary", data=dict(email=club_invalid["email"]), follow_redirects=True
    )
    assert "Invalid email address" in response.data.decode()


def test_logout_status_ok(client, clubs_mocked_data):
    logged_in = client.post(
        "/showSummary",
        data=dict(email=clubs_mocked_data[0]["email"]),
        follow_redirects=True,
    )
    assert logged_in.status_code == 200
    loggin_out = client.get("/logout", follow_redirects=True)
    assert request.path == url_for("index")
    assert loggin_out.status_code == 200
    back_in = client.get("/showSummary")
    assert back_in.status_code == 405


def test_cant_access_without_login(client):
    response = client.get("/showSummary")
    assert response.status_code == 405
