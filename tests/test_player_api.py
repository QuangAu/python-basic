
import json
import sys

from app.schemas.enum.player_position import PlayerPosition

sys.path.append('app')
from app.models.player import PlayerModel

def test_add_player_success(client):
    data = PlayerModel(player_name="Mo Salah", age=33, nationality="Egypt", position="FW", market_value=1000000)
    response = client.post("/players", data=data.model_dump_json().encode('utf-8'))
    assert response.status_code == 201

def test_get_player_success(client):
    response = client.get("/players", params={"player_name": "Salah"})
    data = response.json()
    assert data
    
def test_get_player_failed(client):
    response = client.get("/players", params={"player_name": "some name"})
    data = response.json()
    assert not data