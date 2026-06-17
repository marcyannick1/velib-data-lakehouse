CREATE TABLE IF NOT EXISTS dim_station
(
    station_id BIGINT PRIMARY KEY,

    station_code TEXT,

    name TEXT,

    latitude DOUBLE PRECISION,

    longitude DOUBLE PRECISION,

    capacity INTEGER,

    created_at TIMESTAMP DEFAULT NOW()
);



CREATE TABLE IF NOT EXISTS fact_station_status
(
    id SERIAL PRIMARY KEY,

    station_id BIGINT,

    event_time TIMESTAMP,

    bikes_available INTEGER,

    ebikes_available INTEGER,

    docks_available INTEGER,

    last_reported BIGINT,

    is_renting BOOLEAN,

    is_returning BOOLEAN,

    inserted_at TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY(station_id)
    REFERENCES dim_station(station_id)
);



DROP TABLE IF EXISTS dim_time CASCADE;


CREATE TABLE dim_time
(
    time_id SERIAL PRIMARY KEY,

    date_time TIMESTAMP UNIQUE NOT NULL,

    date DATE NOT NULL,

    hour INTEGER,

    day INTEGER,

    month INTEGER,

    year INTEGER,

    day_of_week INTEGER
);