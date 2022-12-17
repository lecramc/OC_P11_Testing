import server
import pytest 

@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    return server.app.test_client()
   
def test_get_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_with_existing_user(client):
    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"})
    assert response.status_code == 200

def test_login_with_non_existing_user(client):
    response = client.post(
        "/showSummary",
        data={"email": "user@simplylift.co"}, follow_redirects=True)
    assert b"Email does not exist" in response.data


def test_get_book(client):
    response = client.get("/book/Fall Classic/Simply Lift")
    assert response.status_code == 200

def test_get_book_with_passed_event(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert (b"Cannot book past competitions"
            in response.data)


def test_purchase_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": 3,
            "competition": "Fall Classic",
            "club": "Simply Lift"})
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

def test_purchase_more_twelve_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": 15,
            "competition": "New Classic",
            "club": "Simply Lift"})
    assert b"You cannot book more than 12 places" in response.data


def test_get_points_display(client):
    response = client.get("/pointsBoard")
    assert response.status_code == 200



def test_logout_redirect(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert (b"Welcome to the GUDLFT Registration Portal!"
            in response.data)