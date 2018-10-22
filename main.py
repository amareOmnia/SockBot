import client_mgmt as d
import queries as q
import manipulator as m

test = q.subTest

# initializes connection to BigQuery API
client = d.Data()

# sends query to database and returns string
results = client.ping_query(test)

# save raw string to JSON file (list of dicts)
client.update_json(results)
client.update_json(m.filter())