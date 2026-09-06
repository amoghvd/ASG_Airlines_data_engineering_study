SELECT
    source,
    destination,
    COUNT(*) AS total_flights,
    AVG(flight_duration_minutes) AS avg_duration_minutes,
    SUM(is_overnight) AS overnight_flights,
    SUM(duration_anomaly) AS anomaly_count
FROM fact_flight
GROUP BY source, destination
ORDER BY total_flights DESC;
