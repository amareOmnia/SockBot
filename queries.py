subTest = '''SELECT body,link_id,parent_id 
FROM [fh-bigquery:reddit_comments.2017_04] 
WHERE score>6 
AND body!='[removed]' 
AND body!='[deleted]' 
AND subreddit='philosophy' OR subreddit = 'academia'
LIMIT 2000'''

# designated json file path (must exist)
json_file = 'data/RawData.json'

# substrings to be removed from all comments
remove = ['http', 'fuck', 'idiot']