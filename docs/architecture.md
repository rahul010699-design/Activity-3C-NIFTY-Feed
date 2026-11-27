

\# NIFTY Option Feed - Architecture



\## 1. Current Local Architecture



The application runs two Python services using Docker Compose.



\- Feed Service: Generates synthetic NIFTY option-chain data.

\- Snapshot Storage: Stores current and previous snapshots.

\- Local Event Publishing: Sends an event to the alerter.

\- Alerter Service: Evaluates PCR and India VIX thresholds.

\- Alert Storage: Stores triggered alerts in alerts.log.

\- Docker Compose: Runs both services.



\## 2. Target GCP Architecture



This is the intended assignment architecture. It has not yet been deployed.



\- Cloud Scheduler: Triggers collection every five minutes.

\- Cloud Run Feed: Runs the feed application.

\- Cloud Storage: Stores raw JSON snapshots.

\- BigQuery: Stores option snapshots and chain metrics.

\- Pub/Sub: Sends snapshot-ready events.

\- Cloud Run Alerter: Evaluates alert conditions.

\- Secret Manager: Stores broker credentials securely.

\- Cloud Logging: Collects application logs.

\- Cloud Monitoring: Tracks metrics and alerts.

\- Artifact Registry: Stores container images.



\## 3. Security



\- Cloud Run services should remain private.

\- Scheduler and Pub/Sub should use OIDC authentication.

\- Service accounts should follow least-privilege IAM.

\- Credentials should be stored in Secret Manager.

\- Never commit credentials to GitHub.



\## 4. Deployment Status



| Component | Status |

|---|---|

| Feed service | Local tested |

| Alerter service | Local tested |

| Docker containers | Tested |

| Mock snapshot generation | Tested |

| Local alert processing | Tested |

| Cloud Storage | Pending |

| BigQuery | Pending |

| Pub/Sub | Pending |

| Cloud Run | Pending |

| Cloud Scheduler | Pending |

| Cloud Monitoring | Pending |



GCP deployment is pending due to the project's billing account restriction.



