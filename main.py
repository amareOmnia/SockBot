import client_mgmt as d

# initializes connection to BigQuery API
client = d.Data()

testQ = '''SELECT body,link_id,parent_id,subreddit 
FROM [fh-bigquery:reddit_comments.2017_04] 
WHERE subreddit='philosophy' 
AND score>6 
AND body!='[removed]' 
AND body!='[deleted]' 
LIMIT 1000'''

results = client.ping_query(testQ)
print(results)