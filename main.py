import client_mgmt as d
import queries as q
# initializes connection to BigQuery API
client = d.Data()

test = q.subTest

results = client.ping_query(test)