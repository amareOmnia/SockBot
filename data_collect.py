# new attempt at collecting data. BigQuery now has a dataset of reddit comments
# thats actually standardized. Much easier than database.py

import bigquery
import bigQauth as b

email = b.client_email
print(email)

client = bigquery.client.get_client(project_id = "3ff2a19e84da941f3696af27bb5dc0ece073a71d", service_account=email, private_key_file="credentials.p12", readonly="true")
print(client)