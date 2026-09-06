# ASG Airlines — End-to-End Data Engineering & Power BI Analytics

## Project

ASG Airlines is an end-to-end airline analytics case study using Azure Data Lake Storage Gen2, Azure Data Factory, Azure Databricks/PySpark and Power BI. The source workbook is `UseCase - Airlines.xlsx` with flights, bookings, payments and passengers.

## Architecture

```text
UseCase - Airlines.xlsx
        |
        v
Azure Data Lake Storage Gen2
  BRONZE / SILVER / GOLD / QUARANTINE
        |
        v
Azure Data Factory
        |
        v
Azure Databricks / PySpark
        |
        v
Power BI
```

## Azure resources

Resource Group: `ASG-Airlines-RG`

Storage Account: `asgairlines`

Data Factory: `ASG-Airlines-ADF`

Databricks: `ASG-Airlines-DB`

Compute: `ASG-Airlines-Compute`

Access Connector: `ASG-Airlines-Connector`

ADF linked service: `LS_ADLS_ASG`

Databricks notebook: `NB_ASG_Airlines_Silver`

## Data Lake layout

```text
bronze/
  flights/
  bookings/
  payments/
  passengers/

silver/
  flights/
  bookings/
  payments/
  passengers/

gold/
  fact_flight/
  dim_airline/
  dim_route/
  dim_date/
  kpi/

quarantine/
  flights/
  bookings/
  payments/
  passengers/
```

## Source profiling

| Dataset | Rows | Main purpose |
|---|---:|---|
| flights | 1,020 | Flight schedules and routes |
| bookings | 1,000 | Booking transactions |
| payments | 1,000 | Payment transactions |
| passengers | 1,039 | Passenger master data |

Important source findings include 41 missing airline values, 31 `UNKNOWN` airline values and 15 exact duplicate flight rows. The flight data also contains 6F codes treated as corrupted IndiGo codes and one anomalous SJ192 timing record.

Bookings contain 45 missing statuses and 30 `INVALID` statuses. Payments contain 48 missing amounts and 30 `INVALID` amounts. Passenger data contains 39 duplicate passenger IDs and 10 missing last names.

Referential integrity was clean: booking-to-flight, booking-to-passenger and payment-to-booking references resolve.

## ADF ingestion

The workbook is placed in Bronze and ADF converts each sheet to CSV.

Pipelines:

```text
PL_ASG_Flights_Bronze
PL_ASG_Bookings_Bronze
PL_ASG_Payments_Bronze
PL_ASG_Passengers_Bronze
```

## PySpark transformation

Flight airline codes are standardized:

```text
AI -> Air India
6F / 6E -> IndiGo
SJ -> SpiceJet
UK -> Vistara
```

Flight duration is calculated from arrival and departure timestamps rather than trusting the malformed Excel duration representation. Exact duplicate rows are removed. Invalid timing records are quarantined.

Booking status is standardized and missing/invalid values become `UNKNOWN`.

Payment amounts are converted to numeric values and missing/invalid amounts are safely handled.

Passengers are deduplicated by `passenger_id` using a deterministic quality score that favors complete names, valid 12-digit Aadhaar, email and phone.

## Gold model

The recommended Power BI star schema contains:

```text
fact_flight
fact_booking
fact_payment

dim_airline
dim_route
dim_date
dim_passenger
```

Direct PII should not be exposed in the executive model. Names, Aadhaar, passport, phone, email and emergency-contact fields should be excluded or masked.

## Power BI Executive Overview

Recommended KPIs:

```text
Total Flights
Total Bookings
Total Payment Value
Active Airlines
Average Flight Duration
```

Recommended visuals include bookings by airline, payment/revenue trend, flights by destination, booking-status distribution and top routes. Slicers should include airline, source, destination, date and booking status.

## Power BI Data Quality Dashboard

Recommended KPIs:

```text
Total Source Records
Valid Records
Quarantined Records
Duplicate Records
Missing/Invalid Records
Data Quality %
```

Recommended visuals include quality by dataset, issue-type distribution, missing/invalid records by field, duplicate records by dataset, quarantine count and referential-integrity status.

## DAX

```DAX
Total Flights = DISTINCTCOUNT(fact_flight[flight_id])

Total Bookings = DISTINCTCOUNT(fact_booking[booking_id])

Total Payment Value = SUM(fact_payment[amount])

Average Flight Duration = AVERAGE(fact_flight[duration_minutes])

Data Quality % =
DIVIDE([Valid Records], [Total Source Records], 0)
```

## Deliverables

This package contains a Power BI-ready README, DAX measures, theme JSON, architecture notes and dashboard reference image.

## PBIX limitation

A native `.pbix` file cannot be reliably authored in this environment because PBIX is a Microsoft proprietary Power BI Desktop format. I therefore have not created a fake `.pbix` and called it valid.

The included assets are intended to be loaded into Power BI Desktop to create the actual report.

## Build sequence

```text
Raw Excel
  -> Bronze
  -> ADF ingestion
  -> Databricks cleansing
  -> Silver
  -> Gold star schema
  -> Power BI
  -> Executive Overview
  -> Data Quality Dashboard
```
