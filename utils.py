import json
import os

teams_file_path = os.path.join(os.path.dirname(__file__), 'dummy_data', 'teams.json')

with open(teams_file_path, 'r') as file:
    teams = json.load(file)

games_file_path = os.path.join(os.path.dirname(__file__), 'dummy_data', 'bruins_away_games_dict.json')

with open(games_file_path, 'r') as file:
    games = json.load(file)

def get_team_names():
    return [{ "id": index + 1, "name": team['name'] } for index, team in enumerate(get_teams())]

def get_games(team=None):
    if team:
        return games[team]
    return games

def get_teams():
    return teams
    return [{
        "id": 1,
        "name": "Chicago Blackhawks"
    },
     {
        "id": 2,
        "name": "Detroit Red Wings"
    },
     {
        "id": 3,
        "name": "Montreal Canadiens"
    },
     {
        "id": 4,
        "name": "New York Rangers"
    },
    {
        "id": 5,
        "name": "Toronto Maple Leafs"
    },]

def getTeam(team_id):
    return get_teams()[team_id]