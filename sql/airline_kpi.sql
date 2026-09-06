SELECT
    a.airline,
    COUNT(*) AS total_flights,
    AVG(f.flight_duration_minutes) AS avg_duration_minutes,
    SUM(f.is_overnight) AS overnight_flights,
    SUM(f.duration_anomaly) AS anomaly_count
FROM fact_flight f
JOIN dim_airline a ON f.airline_key = a.airline_key
GROUP BY a.airline
ORDER BY total_flights DESC;
