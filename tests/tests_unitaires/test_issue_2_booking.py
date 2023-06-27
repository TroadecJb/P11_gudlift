import pytest
from flask import url_for, request

import server


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


def test_purchase_more_than_available(
    client, competitions_mocked_data, clubs_mocked_data
):
    places = 9
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions_mocked_data[1]["name"],
            "club": clubs_mocked_data[1]["name"],
            "places": str(places),
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        f"There is only {competitions_mocked_data[1]['numberOfPlaces']} available for this competiton."
        in response.data.decode()
    )


def test_purchase_places_clubs_points_deduced(
    client, competitions_mocked_data, clubs_mocked_data
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
    client, competitions_mocked_data, clubs_mocked_data
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
