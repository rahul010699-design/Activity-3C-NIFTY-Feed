

\# NIFTY Option Feed - Operations Runbook



\## 1. Purpose



This runbook explains how to operate and troubleshoot the local mock-mode NIFTY feed and alerting application.



\## 2. Prerequisites



\- Windows 11

\- Docker Desktop

\- Docker Compose

\- Git



\## 3. Start the Application



Open PowerShell in the project root directory.



Build and start both services:



&#x20;   docker compose up --build -d



Check container status:



&#x20;   docker compose ps



Both nifty-feed and nifty-alerter should show Running.



\## 4. Health Checks



Feed service:



&#x20;   Invoke-RestMethod http://localhost:8000/health



Expected status: healthy



Alerter service:



&#x20;   Invoke-RestMethod http://localhost:8001/health



Expected status: healthy



\## 5. Collect a Snapshot



Execute:



&#x20;   Invoke-RestMethod -Method Post -Uri "http://localhost:8000/collect"



The feed generates a synthetic NIFTY snapshot and sends an event to the alerter.



\## 6. Verify Snapshot



Execute:



&#x20;   Invoke-RestMethod http://localhost:8000/latest



Check the timestamp, NIFTY price, India VIX, PCR and option-chain records.



\## 7. Verify Alerts



Inspect the alert log:



&#x20;   Get-Content .\\data\\alerts.log



The alerter checks:



\- PCR below 0.70

\- PCR above 1.30

\- India VIX increase above 10%



\## 8. Troubleshooting



\### Containers are not running



&#x20;   docker compose ps

&#x20;   docker compose logs



\### Feed service is unavailable



&#x20;   docker compose logs feed



\### Alerter service is unavailable



&#x20;   docker compose logs alerter



\### Rebuild the application



&#x20;   docker compose down

&#x20;   docker compose up --build -d



\## 9. Stop the Application



&#x20;   docker compose down



\## 10. Operational Notes



\- The application currently uses synthetic mock data.

\- No broker credentials are required.

\- No real trades are executed.

\- No NSE website scraping is performed.

\- Generated local data is stored in the data directory.

\- GCP deployment is pending due to a billing account restriction.



\## 11. Target Cloud Operations



The planned GCP deployment will use Cloud Run, Cloud Scheduler, BigQuery, Cloud Storage, Pub/Sub, Secret Manager and Cloud Monitoring.



These cloud operations have not yet been tested because the GCP deployment is pending.





