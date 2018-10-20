# new attempt at collecting data. BigQuery now has a dataset of reddit comments
# that's actually standardized. Much easier than database.py
import time
import bigquery
import bigQauth as b

class Data:
  def __init__(self):
    email = b.client_email
    project = b.project_id
    key = b.credentials

    self.client = bigquery.client.get_client(project_id = project, service_account=email, private_key_file=key, readonly="true")

  def ping_query(self, query):
    job, result = self.client.query(query, timeout=10)
    complete, progress = self.client.check_job(job)
    print ("Progress:", progress, "elements")
    if complete: 
      print("query complete")
    return result