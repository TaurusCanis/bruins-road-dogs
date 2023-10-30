CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE games (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT,
    windowsTimeZoneId TEXT,
    startDateTimeUtc TEXT NOT NULL,
    endDateTimeUtc TEXT,
    startDateTimeLocal TEXT,
    isAllDayEvent BOOLEAN,
    home_team_id INTEGER,
    FOREIGN KEY (home_team_id) REFERENCES teams(id)
);

CREATE TABLE arenas (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    team_id INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- @DOWN

-- Drop the tables
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS arenas;
DROP TABLE IF EXISTS teams;