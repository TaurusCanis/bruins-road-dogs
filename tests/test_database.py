from app import app, get_teams, get_team, get_games

def test_get_teams(client, test_db):
    with app.app_context():  # Push an application context
        assert len(get_teams(test_db)) == 31

def test_get_team(client, test_db):
    with app.app_context():  # Push an application context
        team = get_team(test_db, 2)
        assert team[1] == "Philadelphia Flyers"

def test_get_games(client, test_db):
    with app.app_context():
        games = get_games(test_db, 3)
        assert len(games) == 2
