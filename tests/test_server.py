import pytest
from Python_Testing.server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_competitions(mocker):
    return mocker.patch('Python_Testing.server.competitions',
                        [{'name': 'Competition1', "date": "2020-03-27 10:00:00", 'numberOfPlaces': 15},
                         {'name': 'Competition2', "date": "2025-10-22 13:30:00", 'numberOfPlaces': 5},
                         {'name': 'Competition3', "date": "2024-10-22 16:30:00", 'numberOfPlaces': 0}])


@pytest.fixture
def mock_club(mocker):
    return mocker.patch('Python_Testing.server.clubs', [{'name': 'Club1', "email": "john@simplylift.co", "points": 13},
                                                        {'name': 'Club2', "email": "admin@irontemple.com",
                                                         "points": 4}])


def test_purchase_exceed_maximum_points(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition2',
        'club': 'Club2',
        'places': '5'
    })

    assert response.status_code == 200
    assert b'You do not have enough points to book!' in response.data
    assert competitions[1]['numberOfPlaces'] == 5
    assert clubs[1]['points'] == 4


def test_purchase_place(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition2',
        'club': 'Club2',
        'places': '3'
    })

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert competitions[1]['numberOfPlaces'] == 2
    assert clubs[1]['points'] == 1