def test_index_route(client):
    response = client.get('/')
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Check if a specific string is present in the rendered HTML
    assert b"Select Team" in response.data

def test_teams_id_route(client):
    response = client.get('/teams/1/')
    assert response.status_code == 200
    assert b"Chicago Blackhawks" in response.data

def test_non_existent_team(client):
    response = client.get('/teams/99999/')  # Assuming 99999 is an ID that doesn't exist
    
    # Check if the response status code is 404 (Not Found)
    assert response.status_code == 404

def test_team_invalid_id(client):
    response = client.get('/teams/abc/')
    assert response.status_code == 404

