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


def test_purchasePlaces_with_competition_available(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition2',
        'club': 'Club1',
        'places': '2'
    })

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert clubs[0]['points'] == 11
    assert competitions[1]['numberOfPlaces'] == 3


def test_purchasePlaces_with_tournament_passed(client, mock_competitions, mock_club):
    # create test data
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition1',
        'club': 'Club1',
        'places': '2'
    })

    assert response.status_code == 200
    assert b'The competition has already passed' in response.data
    assert clubs[0]['points'] == 13
    assert competitions[0]['numberOfPlaces'] == 15
