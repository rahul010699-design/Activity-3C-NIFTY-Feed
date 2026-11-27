# NIFTY Option Feed on GCP

## Project Overview

This project implements a mock-mode NIFTY options feed and alerting system. It generates synthetic NIFTY market snapshots, evaluates option-chain metrics, and records alerts.

The application is containerized using Docker and Docker Compose.

**Current status:** Local Docker implementation completed and tested. GCP deployment is pending due to a billing account restriction.

## Architecture

- Feed Service: Generates mock NIFTY option-chain snapshots.
- Alerter Service: Evaluates PCR and India VIX thresholds.
- Docker Compose: Runs both services locally.
- Shared Data Volume: Stores snapshots and alert logs.

## Technology Stack

- Python
- Docker
- Docker Compose
- JSON
- Google Cloud Platform (target deployment)

## Project Structure

    Activity-3C-NIFTY-Feed/
    ├── feed/
    │   ├── main.py
    │   └── Dockerfile
    ├── alerter/
    │   ├── main.py
    │   └── Dockerfile
    ├── data/
    ├── docs/
    ├── docker-compose.yml
    ├── .gitignore
    └── README.md

## Run Locally

Start both services:

    docker compose up --build -d

Check running containers:

    docker compose ps

## Health Checks

Feed service:

    Invoke-RestMethod http://localhost:8000/health

Alerter service:

    Invoke-RestMethod http://localhost:8001/health

## Collect a Mock Snapshot

    Invoke-RestMethod -Method Post -Uri "http://localhost:8000/collect"

## View Latest Snapshot

    Invoke-RestMethod http://localhost:8000/latest

## Stored Data

The application stores generated data in the local data/ directory:

- latest_snapshot.json
- previous_snapshot.json
- alerts.log

## Alert Conditions

- PCR below 0.70
- PCR above 1.30
- India VIX increase above 10%

## Stop Services

    docker compose down

## Important Notes

- This implementation uses synthetic mock data.
- It does not connect to a broker or perform real trades.
- It does not scrape NSE websites.
- No API keys or credentials are stored in the source code.
- GCP deployment is not yet completed.

## Future GCP Deployment

The intended GCP architecture includes:

- Cloud Run
- Cloud Scheduler
- Cloud Storage
- BigQuery
- Pub/Sub
- Secret Manager
- Cloud Monitoring
- Artifact Registry
