

\# Incident Note - NIFTY Option Feed



\## 1. Incident Summary



\*\*Incident:\*\* GCP resource creation blocked by billing account restriction.



\*\*Affected project:\*\* devops-activity-3b



\*\*Region:\*\* asia-south1



\*\*Impact:\*\* Cloud Storage bucket creation failed, preventing completion of the cloud deployment.



\## 2. Observed Error



During Cloud Storage bucket creation, Google Cloud returned:



HTTP 403: The billing account for the owning project is disabled in state delinquent.



The billing overview also indicated that the billing account had a payment-related restriction.



\## 3. Investigation



\- Verified the configured GCP project.

\- Verified that billing was associated with the project.

\- Checked the billing status.

\- Confirmed that the storage bucket was not created.

\- Avoided creating additional billable cloud resources.



\## 4. Resolution and Workaround



Cloud deployment was postponed.



To continue development without creating additional GCP resources:



\- Implemented the feed service locally.

\- Implemented the alerter service locally.

\- Used synthetic mock NIFTY data.

\- Built Docker images.

\- Started both services using Docker Compose.

\- Verified health endpoints.

\- Executed a snapshot collection request.

\- Verified alert generation and local data persistence.



\## 5. Validation Results



| Test | Result |

|---|---|

| Feed health endpoint | Passed |

| Alerter health endpoint | Passed |

| Mock snapshot generation | Passed |

| Local event delivery | Passed |

| Alert processing | Passed |

| Snapshot persistence | Passed |

| GCP bucket creation | Blocked |



\## 6. Current Status



The local mock-mode implementation is operational.



GCP deployment remains pending until the billing restriction is resolved.



\## 7. Lessons Learned



\- Verify billing status before provisioning cloud resources.

\- Develop and test application components locally where possible.

\- Use mock data to validate application logic without broker credentials.

\- Keep credentials out of source code and Git repositories.

\- Document infrastructure blockers accurately.



