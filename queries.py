init_query = '''SELECT body,id,parent_id 
FROM [fh-bigquery:reddit_comments.2018_04] 
WHERE score>5 
AND body!='[removed]' 
AND body!='[deleted]' 
AND subreddit='philosophy' OR subreddit = 'academia'
'''

# designated json file path (must exist)
json_file = 'data/RawData.json'

# substrings to be removed from all comments
remove = ['http', 'fuck', 'idiot', 'trump']