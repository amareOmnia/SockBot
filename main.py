import client_mgmt as d
import queries as q
test = q.subTest

# initializes connection to BigQuery API
client = d.Data()

# sends query to database and returns string
results = client.ping_query(test)

# saves string to JSON file
client.create_json(results)