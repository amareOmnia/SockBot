# manipulates JSON file
from os.path import abspath
import json

import queries as q

def filter():
  # opens path from query config, writes data to dict
  data_dict = json.load(open(q.json_file, mode='r', encoding='utf-8'))
  print('json data prepped for filtering...')
  delete_count = 0
  total_good = len(data_dict)

  # iterates through defined bad contents, and removes them from list
  for substring in q.remove:
    bad_indexes = []

    for i, comment in enumerate(data_dict):
      # creates index list of all comments with prohibited words
      if comment['body'].find(substring) != -1:
        bad_indexes.append(i)
        
    print(len(bad_indexes), 'forbidden comments found with text: "'+ substring +'"')

    bad_length = len(bad_indexes) - 1
    for j in range(bad_length, -1, -1):
      # goes through indexes backwards and deletes bad comments
      del data_dict[bad_indexes[j]]
      delete_count += 1
      total_good -= 1

  print('filtered comments:', delete_count)
  print('remaining comments:', total_good)
  return data_dict


def filter_quotes():
  # opens path from query config, writes data to dict
  data_dict = json.load(open(q.json_file, mode='r', encoding='utf-8'))
  print('json data prepped for filtering...')
  delete_count = 0
  total_good = len(data_dict)

  # iterates through defined bad contents, and removes them from list
  for substring in ["'",'"']:
    bad_indexes = []

    for i, comment in enumerate(data_dict):
      # creates index list of all comments with prohibited words
      if comment['body'].find(substring) != -1:
        bad_indexes.append(i)
        
    print(len(bad_indexes), 'forbidden comments found with text: "'+ substring +'"')

    bad_length = len(bad_indexes) - 1
    for j in range(bad_length, -1, -1):
      # goes through indexes backwards and deletes bad comments
      del data_dict[bad_indexes[j]]
      delete_count += 1
      total_good -= 1

  print('filtered comments:', delete_count)
  print('remaining comments:', total_good)
  return data_dict