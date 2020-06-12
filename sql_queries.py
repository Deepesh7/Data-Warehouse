import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events
    (
        artist            TEXT,
        auth              TEXT,
        first_name        TEXT,
        gender            TEXT,
        item_in_session   INTEGER,
        last_name         TEXT,
        length            DECIMAL,
        level             TEXT,
        location          TEXT,
        method            TEXT,
        page              VARCHAR,
        registraton       FLOAT,
        session_id        INTEGER,
        song              TEXT,
        status            INTEGER,
        ts                TIMESTAMP,
        user_agent        TEXT,
        user_id           INTEGER
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
    (
        num_songs         INTEGER,
        artist_id         TEXT,
        artist_latitude   DECIMAL,
        artist_longitude  DECIMAL,
        artist_location   TEXT,
        artist_name       TEXT,
        song_id           TEXT,
        title             TEXT,
        duration          DECIMAL,
        year              INTEGER
    );

""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id   INTEGER    IDENTITY(0,1)  PRIMARY KEY,
        start_time    TIMESTAMP  NOT NULL REFERENCES time(start_time) SORTKEY DISTKEY,
        user_id       INTEGER    NOT NULL REFERENCES users(user_id),
        level         TEXT,
        song_id       TEXT       REFERENCES songs(song_id),
        artist_id     TEXT       REFERENCES artists(artist_id),
        session_id    INTEGER,
        location      TEXT, 
        user_agent    TEXT
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id      INTEGER    SORTKEY PRIMARY KEY,
        first_name   TEXT,
        last_name    TEXT,
        gender       TEXT,
        level        TEXT
    )diststyle all;
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs
    (
        song_id     TEXT       SORTKEY PRIMARY KEY,
        title       TEXT,
        artist_id   TEXT,
        year        INTEGER,
        duration    FLOAT      NOT NULL
    )diststyle all;
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists
    (
        artist_id    TEXT      SORTKEY PRIMARY KEY,
        name         TEXT,
        location     TEXT,
        latitude     DECIMAL,
        longitude    DECIMAL
    )diststyle all;
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time
    (
        start_time    timestamp  SORTKEY DISTKEY PRIMARY KEY,
        hour          INTEGER,
        day           INTEGER,
        week          INTEGER,
        month         INTEGER,
        year          INTEGER,
        weekday       TEXT
    );
""")

# STAGING TABLES
log_data = config.get('S3','log_data')
log_json_path = config.get('S3', 'log_jsonpath')
song_data = config.get('S3', 'song_data')
roleArn = config.get('IAM_ROLE', 'arn')

staging_events_copy = ("""
    COPY staging_events FROM {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON {json_path}
    timeformat as 'epochmillisecs';
""").format(data_bucket=log_data, role_arn = roleArn, json_path = log_json_path)

staging_songs_copy = ("""
    COPY staging_songs FROM {data_bucket}
    credentials 'aws_iam_role={role_arn}'
    region 'us-west-2' format as JSON 'auto';
""").format(data_bucket=song_data, role_arn = roleArn)

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT e.ts as start_time,
           e.user_id as user_id,
           e.level as level,
           s.song_id as song_id,
           s.artist_id as artist_id,
           e.session_id as session_id,
           e.location as location,
           e.user_agent as user_agent
    FROM staging_events e
    JOIN staging_songs s ON (e.song = s.title AND e.artist = s.artist_name)
    WHERE e.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
        SELECT  DISTINCT(user_id) AS user_id,
                first_name,
                last_name,
                gender,
                level
        FROM staging_events
        WHERE user_id IS NOT NULL
        AND page = 'NextSong';
""")

song_table_insert = ("""
    INSERT INTO songs(song_id, title, artist_id, year, duration)
    SELECT DISTINCT(song_id) as song_id, 
           title, 
           artist_id, 
           year, 
           duration 
    FROM staging_songs 
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO artists(artist_id, name, location, latitude, longitude)
    SELECT DISTINCT(artist_id) as artist_id,
           artist_name as name,
           artist_location as location,
           artist_latitude as latitude,
           artist_longitude as longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO time(start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT(ts) as start_time,
           EXTRACT(hour FROM ts) as hour,
           EXTRACT(day FROM ts) as day,
           EXTRACT(week FROM ts) as week,
           EXTRACT(month FROM ts) as month,
           EXTRACT(year FROM ts) as year,
           EXTRACT(dayofweek FROM ts) as weekday
    FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [user_table_insert, artist_table_insert, song_table_insert, time_table_insert, songplay_table_insert]