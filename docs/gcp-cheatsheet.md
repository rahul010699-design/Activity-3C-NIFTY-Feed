\# GCP Cheat Sheet – Activity 3C



\*\*Project:\*\* NIFTY Options Feed on GCP  

\*\*Region:\*\* asia-south1  

\*\*Mode:\*\* MOCK



> These are reference commands for the planned GCP deployment. Due to the project's billing account restriction, the cloud resources have not yet been deployed or verified.



\## 1. Set GCP project and region



```bash

gcloud config set project YOUR\_PROJECT\_ID

gcloud config set compute/region asia-south1

gcloud config get-value project

gcloud config get-value compute/region

```



\## 2. BigQuery



\### Create dataset



```bash

bq --location=asia-south1 mk -d nifty\_feed

```



\### Create option snapshots table



```sql

CREATE TABLE `YOUR\_PROJECT\_ID.nifty\_feed.option\_snapshots` (

&#x20; timestamp TIMESTAMP,

&#x20; symbol STRING,

&#x20; underlying\_price FLOAT64,

&#x20; strike\_price FLOAT64,

&#x20; option\_type STRING,

&#x20; open\_interest INT64,

&#x20; last\_traded\_price FLOAT64,

&#x20; data\_mode STRING

)

PARTITION BY DATE(timestamp);

```



\### Create chain metrics table



```sql

CREATE TABLE `YOUR\_PROJECT\_ID.nifty\_feed.chain\_metrics` (

&#x20; timestamp TIMESTAMP,

&#x20; symbol STRING,

&#x20; pcr FLOAT64,

&#x20; india\_vix FLOAT64,

&#x20; underlying\_price FLOAT64,

&#x20; data\_mode STRING

)

PARTITION BY DATE(timestamp);

```



\### Verify tables



```bash

bq ls nifty\_feed

```



\### Query recent snapshots



```sql

SELECT \*

FROM `YOUR\_PROJECT\_ID.nifty\_feed.option\_snapshots`

ORDER BY timestamp DESC

LIMIT 10;

```



\### Query chain metrics



```sql

SELECT timestamp, symbol, pcr, india\_vix

FROM `YOUR\_PROJECT\_ID.nifty\_feed.chain\_metrics`

ORDER BY timestamp DESC

LIMIT 10;

```



\## 3. Cloud Scheduler



\### Required schedule



| Setting | Value |

|---|---|

| Job name | nifty-collect-5min |

| Frequency | Every 5 minutes |

| Cron | `\*/5 9-15 \* \* 1-5` |

| Time zone | Asia/Kolkata |

| Target | HTTP |

| Endpoint | Private Cloud Run `/collect` |

| Authentication | OIDC |

| Service account | sa-scheduler-invoker |



\### Create scheduler job



Replace the placeholders with the actual project ID and deployed Cloud Run URL.



```bash

gcloud scheduler jobs create http nifty-collect-5min \\

&#x20; --location=asia-south1 \\

&#x20; --schedule="\*/5 9-15 \* \* 1-5" \\

&#x20; --time-zone="Asia/Kolkata" \\

&#x20; --uri="https://YOUR\_CLOUD\_RUN\_URL/collect" \\

&#x20; --http-method=POST \\

&#x20; --oidc-service-account=sa-scheduler-invoker@YOUR\_PROJECT\_ID.iam.gserviceaccount.com \\

&#x20; --oidc-token-audience="https://YOUR\_CLOUD\_RUN\_URL"

```



\### Manually trigger the job



```bash

gcloud scheduler jobs run nifty-collect-5min \\

&#x20; --location=asia-south1

```



\### Verify scheduler job



```bash

gcloud scheduler jobs describe nifty-collect-5min \\

&#x20; --location=asia-south1

```



\## 4. Useful BigQuery and Scheduler commands



```bash

\# List BigQuery datasets

bq ls



\# List tables

bq ls nifty\_feed



\# Describe a table

bq show nifty\_feed.option\_snapshots



\# List scheduler jobs

gcloud scheduler jobs list --location=asia-south1



\# View scheduler job details

gcloud scheduler jobs describe nifty-collect-5min --location=asia-south1



\# Run scheduler manually

gcloud scheduler jobs run nifty-collect-5min --location=asia-south1

```



\## 5. Important concepts



\- \*\*BigQuery dataset:\*\* A logical container for related tables.

\- \*\*Partitioning:\*\* Organizes table data by date to improve query efficiency and reduce scanned data.

\- \*\*Cloud Scheduler:\*\* Runs scheduled jobs using cron expressions.

\- \*\*Cron expression:\*\* Defines when a scheduled job executes.

\- \*\*OIDC authentication:\*\* Provides an identity token for authenticated requests to private Cloud Run services.

\- \*\*Time zone:\*\* `Asia/Kolkata` ensures the scheduler uses Indian Standard Time.



\## 6. Deployment status



| Component | Status |

|---|---|

| Local mock feed | Completed and tested |

| Local alerter | Completed and tested |

| Docker Compose | Completed and tested |

| GitHub repository | Published |

| GCP BigQuery | Pending |

| GCP Cloud Scheduler | Pending |

| GCP Cloud Run | Pending |

| GCP Pub/Sub | Pending |

| GCP Monitoring | Pending |



\*\*Note:\*\* Do not interpret the reference commands as evidence that GCP resources have been created. Cloud deployment remains pending due to the billing account restriction.



