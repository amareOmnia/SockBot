import client_mgmt as d
import queries as q
import manipulator as m

query = q.init_query

# initializes connection to BigQuery API
client = d.Data()

# sends query to database and returns string
results = client.ping_query(query)
client.create_json(results)
m.filter_quotes()
# save raw string to JSON file (list of dicts)
# client.update_json(results)
i = 0
new_query, old_data = client.add_id_exceptions_to_query(query)
print(new_query)
new_results = client.ping_query(new_query)
client.update_json(new_results, old_data)

m.filter()
print('done')
