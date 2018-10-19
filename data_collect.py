# new attempt at collecting data. BigQuery now has a dataset of reddit comments
# thats actually standardized. Much easier than database.py

import bigquery

import bigQauth


collector = bigquery.client.get_client()