# Power BI Dashboard Build Guide

## Import
Load these files:
- data/processed/fact_flight.csv
- data/processed/dim_airline.csv
- data/processed/dim_route.csv
- data/processed/dim_date.csv
- data/processed/airline_kpi.csv
- data/processed/route_kpi.csv
- data/processed/daily_kpi.csv
- data/processed/data_quality_summary.csv

## Relationships
- FactFlight[airline_key] -> DimAirline[airline_key]
- FactFlight[route_key] -> DimRoute[route_key]
- FactFlight[date_key] -> DimDate[date_key]

## Measures
Total Flights = COUNTROWS(FactFlight)

Average Flight Duration (min) = AVERAGE(FactFlight[flight_duration_minutes])

Overnight Flights = SUM(FactFlight[is_overnight])

Overnight % = DIVIDE([Overnight Flights], [Total Flights])

Anomalies = SUM(FactFlight[duration_anomaly])

Anomaly % = DIVIDE([Anomalies], [Total Flights])

## Page 1 — Executive Overview
KPI cards: Total Flights, Avg Duration, Overnight %, Anomalies.
Charts: Flights by Airline, Top 10 Routes, Flights by Departure City, Daily Flight Trend.

## Page 2 — Duration Analysis
Average duration by airline, average duration by route, duration distribution, overnight vs non-overnight.

## Page 3 — Route Performance
Route traffic matrix, top routes, average route duration, overnight %, anomaly %.

## Page 4 — Data Quality
Use data_quality_summary.csv and flight_quarantine.csv to show source quality issues and anomaly records.

## Slicers
Airline, Source, Destination, Departure Date, Overnight Flag.
