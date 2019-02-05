# manipulates JSON file
from os.path import abspath
import json

import queries as q

def filter():
  # opens path from query config, writes data to dict
  file_output = open(q.json_file, mode='w+', encoding='utf-8')
  data_dict = json.load(file_output)
  print('Filtering blacklist...')
  delete_count = 0
  total_good = len(data_dict)

  # iterates through defined bad contents, and removes them from list
  for substring in q.remove:
    bad_indexes = []

    for i, comment in enumerate(data_dict):
      # creates index list of all comments with prohibited words
      if comment['body'].find(substring) != -1:
        bad_indexes.append(i)

    bad_length = len(bad_indexes) - 1
    for j in range(bad_length, -1, -1):
      # goes through indexes backwards and deletes bad comments
      del data_dict[bad_indexes[j]]
      delete_count += 1
      total_good -= 1
      
  json.dump(data_dict, file_output)

def filter_quotes():
  # opens path from query config, writes data to dict
  file_output = open('data/RawData.json', mode='r', encoding='utf-8')
  data_dict = json.loads(file_output)
  print('Filtering quotes...')
  delete_count = 0

  # iterates through defined bad contents, and removes them from list
  for substring in ["'",'"']:
    bad_indexes = []

    for i, comment in enumerate(data_dict):
      # creates index list of all comments with prohibited words
      if comment['body'].find(substring) != -1:
        bad_indexes.append(i)
        
    bad_length = len(bad_indexes) - 1
    for j in range(bad_length, -1, -1):
      # goes through indexes backwards and deletes bad comments
      del data_dict[bad_indexes[j]]
      delete_count += 1
      total_good -= 1
      
  json.dump(data_dict, file_output)