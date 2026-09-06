"""
ASG Airlines - End-to-End Data Pipeline
This script is a compact reproducible version of the notebook workflow.
"""
import hashlib
import pandas as pd
import numpy as np

PREFIX_TO_AIRLINE = {"AI": "Air India", "6E": "IndiGo", "6F": "IndiGo", "SJ": "SpiceJet", "UK": "Vistara"}

def sha256(value):
    if pd.isna(value):
        return pd.NA
    return hashlib.sha256(str(value).encode()).hexdigest()

def clean_flights(df):
    df = df.copy()
    df["flight_id_original"] = df["flight_id"].astype("string").str.strip().str.upper()
    df["flight_prefix"] = df["flight_id_original"].str[:2]
    df["flight_id"] = df["flight_id_original"].str.replace(r"^6F", "6E", regex=True)
    df["airline"] = df["airline"].astype("string").str.strip().replace({"UNKNOWN": pd.NA})
    df["airline"] = df["airline"].fillna(df["flight_prefix"].map(PREFIX_TO_AIRLINE))
    df["departure_datetime"] = pd.to_datetime(df["departure_time"], errors="coerce")
    df["arrival_datetime"] = pd.to_datetime(df["arrival_time"], errors="coerce")
    df["is_overnight"] = (df["arrival_datetime"] < df["departure_datetime"]).astype("int8")
    df["arrival_datetime"] = df["arrival_datetime"] + pd.to_timedelta(df["is_overnight"], unit="D")
    df["flight_duration_minutes"] = (
        df["arrival_datetime"] - df["departure_datetime"]
    ).dt.total_seconds() / 60
    df["duration_anomaly"] = (
        df["flight_duration_minutes"].isna()
        | (df["flight_duration_minutes"] <= 0)
        | (df["flight_duration_minutes"] > 480)
    ).astype("int8")
    df["route"] = df["source"].astype("string").str.upper() + " → " + df["destination"].astype("string").str.upper()
    df["flight_id_valid"] = df["flight_id"].str.match(r"^(AI|6E|SJ|UK)\d{3}$", na=False)
    df["record_valid"] = (
        df["flight_id_valid"] & df["airline"].notna() &
        df["departure_datetime"].notna() & df["arrival_datetime"].notna() &
        (df["duration_anomaly"] == 0)
    )
    df["is_duplicate"] = df.duplicated(
        ["flight_id","departure_datetime","source","destination"], keep="first"
    ).astype("int8")
    return df

def main(input_file):
    sheets = pd.read_excel(input_file, sheet_name=None)
    flights = clean_flights(sheets["flights"])
    valid_flights = flights[(flights["record_valid"]) & (flights["is_duplicate"] == 0)].copy()
    return valid_flights

if __name__ == "__main__":
    result = main("UseCase - Airlines.xlsx")
    print(f"Valid analytical flight rows: {len(result)}")
