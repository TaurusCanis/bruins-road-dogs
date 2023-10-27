import sqlite3
import os
import argparse

MIGRATIONS_DIR = 'migrations/'

def create_migrations_table(conn):
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS migrations (
            version TEXT PRIMARY KEY,
            applied_on DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')

def get_applied_migrations(conn):
    with conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS migrations (
            version TEXT PRIMARY KEY,
            applied_on DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        return {row[0] for row in conn.execute('SELECT version FROM migrations')}

def apply_migration(conn, version, direction='up'):
    with open(os.path.join(MIGRATIONS_DIR, version + '.sql')) as f:
        script = f.read()
        up_script, down_script = script.split('-- @DOWN')
        if direction == 'down':
            conn.executescript(down_script)
            with conn:
                conn.execute('DELETE FROM migrations WHERE version = ?', (version,))
        else:
            conn.executescript(up_script)
            with conn:
                conn.execute('INSERT INTO migrations (version) VALUES (?)', (version,))

def get_migrations():
    return sorted(f.split('.')[0] for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.sql'))

def migrate(direction='up'):
    print("Migrating...")
    conn = sqlite3.connect('instance/bruins_road_dogs.db')
    applied = get_applied_migrations(conn)
    print("Applied migrations: ", applied)
    all_migrations = get_migrations() #sorted(f.split('.')[0] for f in os.listdir(MIGRATIONS_DIR) if f.endswith('.sql'))

    if direction == 'up':
        migrations_to_apply = [m for m in all_migrations if m not in applied]
        print("Migrations to apply: ", migrations_to_apply)
        for migration in migrations_to_apply:
            apply_migration(conn, migration, direction)
    else:  # direction == 'down'
        if applied:  # Check if there are any applied migrations
            last_migration = list(applied)[-1]  # Get the last migration
            apply_migration(conn, last_migration, direction)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage database migrations.')
    parser.add_argument('direction', choices=['up', 'down'], help='Direction to apply migrations. Can be "up" or "down".')
    args = parser.parse_args()
    migrate(args.direction)
