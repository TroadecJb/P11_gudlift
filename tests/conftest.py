import pytest
import server
from server import loadClubs, loadCompetitions, competitions, clubs


@pytest.fixture
def client():
    app = server.app
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def club_invalid():
    data = {
        "name": "invalid",
        "email": "not_a_mail_address",
        "points": "0",
    }
    return data


@pytest.fixture(scope="function")
def competitions_mocked_data():
    server.competitions = [
        {
            "name": "future_competition",
            "date": "2023-10-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "future_competition_few_places",
            "date": "2023-11-25 10:00:00",
            "numberOfPlaces": "5",
        },
        {
            "name": "past_competition",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "2",
        },
    ]
    return server.competitions


@pytest.fixture(scope="function")
def clubs_mocked_data():
    server.clubs = [
        {
            "name": "club_valid",
            "email": "club@test.mail",
            "points": "13",
        },
        {
            "name": "other_club_valid",
            "email": "other_club@test.mail",
            "points": "0",
        },
    ]
    return server.clubs


@pytest.fixture(scope="function")
def purchaseRecap_mocked():
    server.purchaseRecap = {}
    return server.purchaseRecap
