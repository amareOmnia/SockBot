init_query = """SELECT replace(body, '\"', '') as body, \
id,parent_id \
FROM [fh-bigquery:reddit_comments.2018_04] \
WHERE rand() <= .3 \
AND score>5 \
AND body!='[removed]' \
AND body!='[deleted]' \
AND subreddit='philosophy' OR subreddit = 'academia'"""

# designated json file path (must exist)
json_file = 'data/RawData.json'

# substrings to be removed from all comments
remove = ['http', 'fuck', 'idiot', 'trump']

def update_query():
  date = init_query[init_query.index('comments')+9:init_query.index('comments')+16]
  new_date = ''
  if int(date[5:6]) == 12:
    new_date = str(int(date[:4]) + 1) + '_01'
  else: 
    if int(date[5:6]) < 9:
      new_date = date[:4] + '_0' + str(int(date[5:6]) + 1)
    else:
      new_date = date[:4] + '_' + str(int(date[5:6]) + 1)
  return init_query.replace(date, new_date)