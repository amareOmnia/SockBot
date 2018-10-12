import sqlite3
import json
from datetime import datetime

# later scaling: loop that builds a larger base
# either by scanning the months or compiling a list....
# for year in range (2008-2014):

# forming range and tools
timeframe = '2015-05'
good_subreddit = ["Philosophy", "AskPhilosophy",]
sql_transaction = []
accept_index = 0
start_row = 0
cleanup = 1000000
connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()


# SQL table formation with correct data types
def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply
    (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, 
    comment TEXT, subreddit TEXT, unix INT, score INT)""")


# removes new lines, changes all quotes to single
def format_data(data):
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace(' " ', " ' ")
    return data


# returns score of comment
def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1 ".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        # print("find_parent", e)
        return False


# returns the text of the parent comment of a reply, and false if there is no parent
def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1 ".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        # print("find_parent", e)
        return False


# analyzes body of text and returns false if too long, short, or if it's omitted.
def acceptable(data,subreddit):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    # Accepted subreddits to collect entries
    elif not ((subreddit.find('Philosophy') > -1) or (subreddit.find('Science') > -1) or
                  (subreddit.find('Academic') > -1) or (subreddit.find('History') > -1)):
        return False
    else:
        return True


def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 5000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

# changes the existing row to new comment
def sql_insert_replace_comment(commentid, parentid,parent, comment, subreddit, time, score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? 
            WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s-UPDATE insertion', str(e))


def sql_insert_has_parent(commentid, parentid, parent, comment, subreddit, time, score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score)
            VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s-PARENT insertion', str(e))


def sql_insert_no_parent(commentid, parentid, comment, subreddit, time, score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) 
            VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s-NO_PARENT insertion', str(e))


# calls on create_table, also starts a counter of total rows created, also parent/reply pairs
if __name__ == "__main__":
    create_table()
    row_counter = 0
    paired_rows = 0

# calls on correct dataset, makes it 'f'
    with open('''/media/cooper/HDD 0/Datasets/Reddit/reddit_data/{}/RC_{}/data'''.format(timeframe.split('-')[0], timeframe), buffering=1000) as f:

        '''for row in f:
            # print(row)
            # time.sleep(555)
            row_counter += 1

            if row_counter > start_row:
                try:
                    row = json.loads(row)
                    parent_id = row['parent_id'].split('_')[1]
                    body = format_data(row['body'])
                    created_utc = row['created_utc']
                    score = row['score']

                    comment_id = row['id']

                    subreddit = row['subreddit']
                    parent_data = find_parent(parent_id)

                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            if acceptable(body,subreddit):
                                sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit,
                                                           created_utc, score)

                    else:
                        if acceptable(body,subreddit):
                            if parent_data:
                                if score >= 2:
                                    sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit,
                                                          created_utc, score)
                                    paired_rows += 1
                            else:
                                sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)
                except Exception as e:
                    print(str(e))

            if row_counter % 100000 == 0:
                print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows,
                                                                              str(datetime.now())), 'Phil. comments:', accept_index)
            if row_counter > start_row:
                if row_counter % cleanup == 0:
                    print("Cleanin up!")
                    sql = "DELETE FROM parent_reply WHERE parent IS NULL"
                    c.execute(sql)
                    connection.commit()
                    c.execute("VACUUM")
                    connection.commit()'''




        for row in f:
            # print(row)
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id'].split('_')[1]
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            comment_id = row['id']
            # index = subreddit.find("philosophy")
            # print(index)
            # print(subreddit)

            # finds parent body
            parent_data = find_parent(parent_id)
            # logic to qualify each comment: must have upvote/s, must be most upvoted reply
            # if (subreddit.find('Philosophy') > -1) or (subreddit.find('Science') > -1) or (subreddit.find('Academic') > -1):
            if score >= 1:                # if subreddit.find('Philosophy') > -1:
                    if acceptable(body,subreddit):
                        accept_index += 1
                        existing_comment_score = find_existing_score(parent_id)
                        if existing_comment_score:
                            if score > existing_comment_score:
                                sql_insert_replace_comment(comment_id, parent_id,parent_data, body, subreddit, created_utc, score)

                        else:
                            if parent_data:
                                sql_insert_has_parent(comment_id, parent_id,parent_data, body, subreddit, created_utc, score)
                                paired_rows += 1
                            else:
                                sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)

            if row_counter % 100000 == 0:
                print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows,
                        str(datetime.now())), 'Phil. comments:', accept_index)

