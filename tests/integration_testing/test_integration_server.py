import json

import pytest
from Python_Testing.server import loadClubs, loadCompetitions, app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_load_clubs():
    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert len(clubs) > 0


def test_load_competitions():
    competitions = loadCompetitions()
    assert isinstance(competitions, list)
    assert len(competitions) > 0


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200



def test_showSummary(client):
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_book(client):
    competitions = loadCompetitions()
    clubs = loadClubs()
    response = client.get('/book/Winter Festival/Simply Lift')
    assert response.status_code == 200


def test_purchasePlaces(client):
    data = dict(competition='Winter Festival', club='Simply Lift', places=1)
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data


def test_display(client):
    clubs = loadClubs()
    response = client.get('/display')
    assert response.status_code == 200
    for club in clubs:
        assert bytes(club['name'], "utf-8") in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


