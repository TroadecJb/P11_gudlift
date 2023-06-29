import pytest
from datetime import datetime
from flask import url_for, request


def test_cant_book_future_competition_ok(
    client, competitions_mocked_data, clubs_mocked_data
):
    response = client.get(
        f"/book/{competitions_mocked_data[0]['name']}/{clubs_mocked_data[0]['name']}"
    )
    assert response.status_code == 200
    assert f"<h2>{competitions_mocked_data[0]['name']}</h2>" in response.data.decode()


def test_can_book_past_competition_ok(
    client, competitions_mocked_data, clubs_mocked_data
):
    response = client.get(
        f"/book/{competitions_mocked_data[2]['name']}/{clubs_mocked_data[0]['name']}"
    )
    assert response.status_code == 200
    assert "Something went wrong-please try again" in response.data.decode()


def test_purchase_places_ok(client, competitions_mocked_data, clubs_mocked_data):
    places = 3
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()


def test_purchase_places_not_enough_points(
    client, competitions_mocked_data, clubs_mocked_data
):
    places = 3
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[1]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Not enough points, you can only book" in response.data.decode()


def test_purchase_over_12_places(client, competitions_mocked_data, clubs_mocked_data):
    places = 13
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        "You can not book more than 12 places for any competition."
        in response.data.decode()
    )


def test_purchase_over_12_split(
    client, competitions_mocked_data, clubs_mocked_data, purchaseRecap_mocked
):
    init_points = clubs_mocked_data[0]["points"]
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": "12",
        },
        follow_redirects=True,
    )

    assert init_points == "13"

    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert clubs_mocked_data[0]["points"] == "1"

    first_purchase_points = clubs_mocked_data[0]["points"]
    second_response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": "2",
        },
        follow_redirects=True,
    )
    second_purchase_points = clubs_mocked_data[0]["points"]
    assert first_purchase_points == "1"
    assert second_purchase_points == "1"
    assert second_response.status_code == 200
    assert (
        "You have already booked the maximum allowed numbers of places."
        in second_response.data.decode()
    )


def test_purchase_more_than_available(
    client, competitions_mocked_data, clubs_mocked_data, purchaseRecap_mocked
):
    places = 9
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[1]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert f"available for this competiton." in response.data.decode()


def test_purchase_places_clubs_points_deduced(
    client, competitions_mocked_data, clubs_mocked_data, purchaseRecap_mocked
):
    club_start_point = int(clubs_mocked_data[0]["points"])
    places = 3
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert int(clubs_mocked_data[0]["points"]) != club_start_point
    assert int(clubs_mocked_data[0]["points"]) == club_start_point - places


def test_purchase_places_competition_places_available_deduced(
    client, competitions_mocked_data, clubs_mocked_data, purchaseRecap_mocked
):
    competitions_available_places_start = int(
        competitions_mocked_data[0]["numberOfPlaces"]
    )
    places = 3
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[0]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()
    assert (
        int(competitions_mocked_data[0]["numberOfPlaces"])
        != competitions_available_places_start
    )
    assert (
        int(competitions_mocked_data[0]["numberOfPlaces"])
        == competitions_available_places_start - places
    )


def test_purchase_places_past_competition(
    client, competitions_mocked_data, clubs_mocked_data
):
    past_competition_date = competitions_mocked_data[2]["date"]
    past_competition_number_places = competitions_mocked_data[2]["numberOfPlaces"]
    currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    places = 3

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[2]["name"],
            "club": clubs_mocked_data[0]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert currentDate > past_competition_date
    assert "This competition is over." in response.data.decode()
    assert (
        competitions_mocked_data[2]["numberOfPlaces"] == past_competition_number_places
    )


def test_showSummary_link_available_based_on_date(
    client, competitions_mocked_data, clubs_mocked_data
):
    response = client.post(
        "/showSummary",
        data=dict(email=clubs_mocked_data[0]["email"]),
        follow_redirects=True,
    )
    assert response.status_code == 200

    assert "/book/future_competition/club_valid" in response.data.decode()
    assert "/book/past_competition/club_valid" not in response.data.decode()
