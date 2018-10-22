# new attempt at collecting data. BigQuery now has a dataset of reddit comments
# that's actually standardized. Much easier than database.py
import time
import json
from os.path import abspath
import bigquery
import bigQauth as b

class Data:
  def __init__(self):
    email = b.client_email
    project = b.project_id
    key = b.credentials
    print('connecting to server...')
    self.client = bigquery.client.get_client(project_id = project, service_account=email, private_key_file=key, readonly="true")

  def ping_query(self, query):
    # sends query to BQ
    print('sending ping...')
    job, result = self.client.query(query, timeout=10)
    # checks if query is complete after 10 secs
    complete, progress = self.client.check_job(job)
    print ("Progress:", progress, "elements")
    if complete: 
      print("query request complete!")
    return result

  def update_json(self, data):
    # takes data as string and writes to JSON file   
    file_output = open(abspath('data/RawData.json'), mode='w', encoding='utf-8')
    json.dump(data, file_output)
    print('json data written to file!')