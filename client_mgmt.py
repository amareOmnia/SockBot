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
    job, result = self.client.query(query, timeout=20)
    complete = False
    # checks if query is complete after 10 secs
    while not complete:
      try:
        complete, progress = self.client.check_job(job)
      except:
        print('Download incomplete. Timeout for 10 more secs...')
        time.sleep(10)
      else:
        complete = True

    print ("Progress:", progress, "elements")
    if complete: 
      print("query request complete!")

    return result

  def create_json(self, data):
    # takes data as string and writes to JSON file   
    file_output = open('data/RawData.json', mode='w+', encoding='utf-8')
    json.dump(data, file_output)
    print('json data written to file!')

  def update_json(self, new_data, old_json):
    file_output = open('data/RawData.json', mode='w+', encoding='utf-8')
    
    
    old_data = list(file_output)
    for comment in new_data:
      old_data.append(comment)    
    json.dump(old_data, file_output)

    print('new json data added to list!')

  def add_id_exceptions_to_query(self, query):
    # adds 'AND link_id NOT LIKE 'existing_id' in multitudes
    data = json.load(open('data/RawData.json', mode='r', encoding='utf-8'))
    # grabs number of existing entries
    comment_quantity = len(data)
    print('number of comments pre-update: ' + str(comment_quantity))
    comment_count = 0
    query_addition = 'AND id NOT IN ('
    used_link_ids = ''
    
    while comment_count<comment_quantity-1:
      # print(data[comment_count]['id'])
      used_link_ids += "'"+ data[comment_count]['id'] +"', "
      comment_count += 1
    used_link_ids += "'"+ data[(comment_quantity-1)]['id'] +"')"

    return (query + query_addition + used_link_ids), data