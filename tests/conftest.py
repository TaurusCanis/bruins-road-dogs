import pytest
import sqlite3
from app import app
import migrate
from scripts.seed_game_and_team_data import seed_db
import os

@pytest.fixture
def client():
    """Provide the test client to test routes."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_db():
    TEST_DB_PATH = 'instance/test_bruins_road_dogs.db'
    # Set up an in-memory test database
    db = sqlite3.connect(TEST_DB_PATH)
    
    # TODO: Initialize the test database (create tables, add test data, etc.)
    migrate.create_migrations_table(db)
    migrations = migrate.get_migrations()
    for migration in migrations:
        migrate.apply_migration(db, migration)

    seed_db(TEST_DB_PATH)

    yield db  # This is the value that will be provided to test functions

    # Clean up
    db.close()
    os.remove(TEST_DB_PATH)  # Delete the database file