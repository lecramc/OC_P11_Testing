import server
import pytest


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    return server.app.test_client()



def test_purchase_place(client):
    """Test de l'achat d'une place par un client"""

    competition_list = server.loadCompetitions()
    club_list = server.loadClubs()
    assert len(club_list) == 3
    assert len(competition_list) == 3

    result_login = client.post("/showSummary",
                               data={
                                   "email": "john@simplylift.co"
                               })
    assert result_login.status_code == 200

    club = server.clubs[0]
    competition = server.competitions[0]

    club_before_point = club["points"]
    competition_before_place = competition['numberOfPlaces']
    result_purchase_place = client.post("/purchasePlaces",
                                        data={
                                            "club": club["name"],
                                            "competition": competition["name"],
                                            "places": 10
                                        })
    assert result_purchase_place.status_code == 200
    assert club["points"] != club_before_point
    assert competition["numberOfPlaces"] != competition_before_place

    result_logout = client.get('/logout')
    assert result_logout.status_code == 302