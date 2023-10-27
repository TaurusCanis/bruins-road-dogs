import os
from flask import Flask, abort, render_template, request, g
from flask_debugtoolbar import DebugToolbarExtension
from .utils import get_teams, get_games, get_team_names
from .filters import format_title, format_date
import sqlite3
import logging

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.INFO)

# Configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
toolbar = DebugToolbarExtension(app)
app.config['DATABASE'] = os.path.join(app.instance_path, 'bruins_road_dogs.db')

def get_db():
	"""
	Connect to the configured database and return the connection. 
	If a connection already exists in the current context, use it.
	"""
	if 'db' not in g:
		g.db = sqlite3.connect(app.config['DATABASE'])
		g.db.row_factory = sqlite3.Row  # Allow for dict-like access to rows
	return g.db

@app.teardown_appcontext
def close_db(e=None):
	"""
	Close the database connection if it exists in the current context.
	"""
	db = g.pop('db', None)

	if db is not None:
		db.close()

# Register custom filters for templates
app.template_filter('format_title')(format_title)
app.template_filter('format_date')(format_date)

def get_teams(db):
	"""
	Retrieve a list of all teams from the database, 
	ordered by their names.
	"""
	# Check if teams are cached, if not, fetch from database
	try:
		if 'teams' not in g:
			logging.info("Fetching teams from database")
			g.teams = db.execute('SELECT id, name FROM teams ORDER BY name').fetchall()
		return g.teams
	except sqlite3.Error as e:
		logging.error(f"Error fetching teams from database: {e}")
		return []

def get_team(db, id):
	"""
	Fetch a single team from the database using its ID.
	"""
	try:
		return db.execute('SELECT * FROM teams WHERE id = ?', (id,)).fetchone() 
	except sqlite3.Error as e:
		logging.error(f"Error fetching team from database: {e}")
		return None

def get_games(db, home_team_id):
	"""
	Retrieve all games where the provided team ID matches 
	the home team's ID.
	"""
	try:
		return db.execute('SELECT * FROM games WHERE home_team_id = ?', (home_team_id,)).fetchall()
	except sqlite3.Error as e:
		logging.error(f"Error fetching games from database: {e}")
		return []

@app.route('/', methods=['GET'])
def index():
	"""
	Main route: Display all teams.
	"""
	db = get_db()
	teams = get_teams(db)  
	return render_template('index.html', teams=teams)

@app.route('/teams/<int:id>/', methods=['GET'])
def teams(id):
	"""
	Display information about a specific team, using its ID, 
	as well as all its games.
	"""
	db = get_db()
	teams = get_teams(db)
	current_team = get_team(db, id)
	if not current_team:
		abort(404)
	games = get_games(db, id)
	return render_template("team.html", current_team=current_team, teams=teams, games=games)
