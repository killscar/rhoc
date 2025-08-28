CREATE TABLE IF NOT EXISTS episodes (
    season INTEGER,
    ep INTEGER,
    title TEXT,
    air_date TEXT,
    synopsis TEXT,
    sources TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    episode_key TEXT,
    source TEXT,
    ts TEXT,
    text TEXT,
    author_hash TEXT,
    score INTEGER,
    permalink TEXT
);

CREATE TABLE IF NOT EXISTS analysis (
    episode_key TEXT,
    sentiment TEXT,
    topics TEXT,
    entities TEXT,
    engagement TEXT
);
