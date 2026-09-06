"""Reusable data quality checks for ASG Airlines."""

import pandas as pd

def validate_required_columns(df, required):
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def validate_flight_duration(df):
    bad = df["flight_duration_minutes"].isna() | (df["flight_duration_minutes"] <= 0)
    return int(bad.sum())

def validate_referential_integrity(bookings, flights, passengers):
    return {
        "booking_to_flight_missing": int((~bookings["flight_id"].isin(flights["flight_id"])).sum()),
        "booking_to_passenger_missing": int((~bookings["passenger_id"].isin(passengers["passenger_id"])).sum()),
    }
