-- ==========================================
-- COUCHE ANALYTIQUE VELIB
-- ==========================================


-- ==========================================
-- KPI GLOBAL
-- ==========================================

CREATE OR REPLACE VIEW vw_global_kpi AS

SELECT

    COUNT(DISTINCT station_id)
        AS total_stations,

    SUM(bikes_available)
        AS total_bikes,

    SUM(ebikes_available)
        AS total_ebikes,

    SUM(docks_available)
        AS total_free_docks,

    ROUND(
        AVG(bikes_available),
        2
    )
        AS avg_bikes_per_station,

    MAX(event_time)
        AS last_update

FROM fact_station_status;



-- ==========================================
-- ETAT DES STATIONS
-- ==========================================

CREATE OR REPLACE VIEW vw_station_availability AS

SELECT

    s.station_id,
    s.station_code,
    s.name,
    s.capacity,

    f.bikes_available,
    f.ebikes_available,
    f.docks_available,


    ROUND(
        (
            f.bikes_available::numeric
            /
            NULLIF(s.capacity,0)
        ) * 100,
        2
    )
        AS occupancy_rate,


    f.event_time


FROM fact_station_status f

JOIN dim_station s
ON s.station_id = f.station_id;




-- ==========================================
-- ALERTES
-- ==========================================

CREATE OR REPLACE VIEW vw_station_alert AS

SELECT

    s.station_id,
    s.station_code,
    s.name,

    f.bikes_available,
    f.ebikes_available,
    f.docks_available,


    CASE

        WHEN f.bikes_available <= 3
            THEN 'LOW_BIKES'

        WHEN f.docks_available <= 2
            THEN 'NO_SPACE'

        ELSE 'OK'

    END AS alert_status,


    f.event_time


FROM fact_station_status f

JOIN dim_station s
ON s.station_id = f.station_id


WHERE

    f.bikes_available <= 3

    OR

    f.docks_available <= 2;




-- ==========================================
-- TOP STATIONS LES PLUS REMPLIES
-- ==========================================

CREATE OR REPLACE VIEW vw_top_busy_stations AS

SELECT

    s.station_id,
    s.station_code,
    s.name,

    s.capacity,

    f.bikes_available,

    ROUND(
        (
        f.bikes_available::numeric
        /
        NULLIF(s.capacity,0)
        ) * 100,
        2
    ) AS occupancy_rate,

    f.event_time


FROM fact_station_status f

JOIN dim_station s
ON s.station_id=f.station_id


ORDER BY occupancy_rate DESC;



-- ==========================================
-- STATIONS VIDES
-- ==========================================

CREATE OR REPLACE VIEW vw_empty_stations AS

SELECT

    s.station_id,
    s.station_code,
    s.name,

    f.bikes_available,
    f.docks_available,

    f.event_time


FROM fact_station_status f

JOIN dim_station s
ON s.station_id=f.station_id


WHERE

    f.bikes_available = 0;




-- ==========================================
-- DISPONIBILITE MOYENNE PAR STATION
-- ==========================================

CREATE OR REPLACE VIEW vw_station_average AS


SELECT

    station_id,

    AVG(bikes_available)
        AS avg_bikes,

    AVG(ebikes_available)
        AS avg_ebikes,

    AVG(docks_available)
        AS avg_docks,


    MIN(event_time)
        AS first_seen,

    MAX(event_time)
        AS last_seen


FROM fact_station_status

GROUP BY station_id;



-- ==========================================
-- HISTORIQUE TEMPS
-- ==========================================

CREATE OR REPLACE VIEW vw_station_history AS


SELECT

    f.station_id,

    s.station_code,

    s.name,

    f.bikes_available,

    f.ebikes_available,

    f.docks_available,

    f.event_time,


    DATE(f.event_time)
        AS day,


    EXTRACT(HOUR FROM f.event_time)
        AS hour


FROM fact_station_status f

JOIN dim_station s

ON s.station_id=f.station_id;



-- ==========================================
-- DASHBOARD METABASE
-- ==========================================

CREATE OR REPLACE VIEW vw_dashboard AS


SELECT

    s.station_id,
    s.station_code,
    s.name,

    s.capacity,

    f.bikes_available,
    f.ebikes_available,
    f.docks_available,


    CASE

        WHEN f.bikes_available <=3
            THEN 'CRITICAL'

        WHEN f.docks_available <=2
            THEN 'FULL'

        ELSE 'NORMAL'

    END AS status,


    f.event_time


FROM fact_station_status f

JOIN dim_station s

ON s.station_id=f.station_id;