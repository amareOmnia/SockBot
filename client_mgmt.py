# new attempt at collecting data. BigQuery now has a dataset of reddit comments
# that's actually standardized. Much easier than database.py
import time
import json
from os.path import abspath
import bigquery
import bigQauth as b

def get_json(mode):
  if mode == 'r':
    return json.load(open('data/RawData.json', mode='r', encoding='utf-8'))
  if mode == 'w':
    return open('data/RawData.json', mode='w+', encoding='utf-8')

class Data:

  def __init__(self):
    email = b.client_email
    project = b.project_id
    key = b.credentials
    print('Connecting to server...')
    self.client = bigquery.client.get_client(project_id = project, service_account=email, private_key_file=key, readonly="true")

  def ping_query(self, query):
    # sends query to BQ
    print('Ping sent...')
    job, result = self.client.query(query, timeout=20)
    complete = False
    # checks if query is complete after delay
    while not complete:
      try:
        complete, progress = self.client.check_job(job)
      except:
        print('Download incomplete. Timeout for 10 more secs...')
        time.sleep(22)
      else:
        complete = True
    print("Data sector downloaded.", progress, "elements retrieved.")
    return result

  def write_json(self, data):
    # takes data as string and writes to JSON file   
    file_output = get_json('w')
    json.dump(data, file_output)
    print('Local data write success.')

  def update_json(self, new_data, old_json):
    # adds each comment from newest query 
    combined_data = []
    for comment in get_json('r'):
      combined_data.append(comment)
    for comment in new_data:
      combined_data.append(comment)    
    print('Local data prepared to rewrite...')
    return combined_data