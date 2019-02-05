import client_mgmt as d
import queries as q
import manipulator as m
import argparse

# define and collect arguments from command line
# parse = argparse.ArgumentParser()
# parse.add_argument('update')
# parse.add_argument('start_date')
# parse.add_argument('output_directory')
# args = parse.parse_args()
query = q.init_query

# initializes connection to BigQuery API
client = d.Data()

# sends query to database and returns string
first_results = client.ping_query(query)
client.write_json(first_results)

# new data is retrieved, then added to local data
i=0
while i < 3:
  new_query = q.update_query()
  new_results = client.ping_query(new_query)
  client.write_json(\
    client.update_json(\
      new_results, first_results))
  i += 1


# m.filter()
print('done')
