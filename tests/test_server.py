import pytest
from Python_Testing.server import app, loadCompetitions, loadClubs


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
                         {'name': 'Competition3', "date": "2024-10-22 16:30:00", 'numberOfPlaces': 0},
                         {'name': 'Competition4', "date": "2024-10-22 16:30:00", 'numberOfPlaces': 15}])


@pytest.fixture
def mock_club(mocker):
    return mocker.patch('Python_Testing.server.clubs', [{'name': 'Club1', "email": "john@simplylift.co", "points": 13},
                                                        {'name': 'Club2', "email": "admin@irontemple.com",
                                                         "points": 4}])


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data


def test_showSummary_with_valid_email(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_showSummary_with_invalid_email(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club
    response = client.post('/showSummary', data={'email': 'unknow@email.co'})
    assert response.status_code == 200
    assert b'This email: unknow@email.co does not exist' in response.data


def test_display(client, mock_club):
    clubs = mock_club
    response = client.get('/display')
    assert response.status_code == 200
    for club in clubs:
        assert bytes(club['name'], "utf-8") in response.data


def test_purchasePlaces_update_points(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition2',
        'club': 'Club2',
        'places': '2'
    })

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert clubs[0]['points'] == 13


def test_purchase_exceed_maximum_points(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition4',
        'club': 'Club1',
        'places': '13'
    })

    assert response.status_code == 200
    assert b'you book more than 12 places' in response.data
    assert competitions[3]['numberOfPlaces'] == 15
    assert clubs[0]['points'] == 13


def test_purchase_maximum_points(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club

    response = client.post('/purchasePlaces', data={
        'competition': 'Competition4',
        'club': 'Club1',
        'places': '12'
    })

    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    assert competitions[3]['numberOfPlaces'] == 3
    assert clubs[0]['points'] == 1


def test_purchase_exceed_maximum_points_available(client, mock_competitions, mock_club):
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


def test_book_with_valid_competition(client, mock_competitions, mock_club):
    competitions = mock_competitions
    clubs = mock_club
    response = client.get('/book/Competition2/Club1')
    assert response.status_code == 200
    assert b"Booking for Competition2" in response.data


def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302


def test_loadClubs():
    clubs = loadClubs()
    assert isinstance(clubs, list)
    assert len(clubs) > 0
    assert isinstance(clubs[0], dict)
    assert 'name' in clubs[0]
    assert 'email' in clubs[0]
    assert 'points' in clubs[0]


def test_loadCompetitions():
    clubs = loadCompetitions()
    assert isinstance(clubs, list)
    assert len(clubs) > 0
    assert isinstance(clubs[0], dict)
    assert 'name' in clubs[0]
    assert 'date' in clubs[0]
    assert 'numberOfPlaces' in clubs[0]