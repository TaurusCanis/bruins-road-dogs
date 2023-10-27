import sqlite3
import json
import os

# Database connection
# conn = sqlite3.connect('instance/bruins_road_dogs.db')

def seed_db(db_path):
    conn = sqlite3.connect(db_path)
    data = get_data()
    populate_data(conn, data)

def insert_team(cursor, team_name):
    cursor.execute('INSERT OR IGNORE INTO teams (name) VALUES (?)', (team_name,))

def insert_game(cursor, game_data):
    home_team_id = cursor.execute('SELECT id FROM teams WHERE name = ?', (game_data['title'].split('@')[-1].strip(),)).fetchone()[0]
    cursor.execute('''
    INSERT INTO games (id, title, startDateTimeUtc, location, home_team_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (game_data['id'], game_data['title'][1:].strip(), game_data['startDateTimeUtc'], game_data['location'], home_team_id))

def populate_data(conn, json_data):
    print("Populating data")
    cursor = conn.cursor()
    
    for game in json_data:
        if game['location'] == "TD Garden":
            continue
        # Extracting home team from title
        home_team = game['title'].split('@')[-1].strip()
        
        # Inserting the home team
        insert_team(cursor, home_team)
        
        # Inserting the game
        insert_game(cursor, game)
        
    conn.commit()
    cursor.close()

def get_data():
   json_file_path = os.path.join(os.path.dirname(__file__), '..', 'dummy_data', 'schedule.json')
   with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data

if __name__ == '__main__':
    seed_db('instance/bruins_road_dogs.db')
    # json_file_path = os.path.join(os.path.dirname(__file__), '..', 'dummy_data', 'schedule.json')
    # with open(json_file_path, 'r') as file:
    #     data = json.load(file)
    #     populate_data(data)
