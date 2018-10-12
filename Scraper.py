

class collect_sub:

    import praw
    reddit = praw.Reddit(client_id='mCJA8WvGuf_ORw',
                         client_secret='l5wPYqOWDoI6pQjAsb82acZHq5w',
                         password='amareomnia',
                         user_agent='philFinder for /u/Soc_Bot',
                         username='Soc_Bot')

    the_self = reddit.user.me()
    print('Hi! This is', theSelf, 'an imma bout da scrape some philosophical scalps.')
    print(reddit.read_only)
    ''' maybe add input for desired sub_reddit: /r/____'''

    '''declares subreddit'''
    sub_reddit = reddit.subreddit("askphilosophy")

    '''collects top submissions'''
    comments_list = list()
    for submission in sub_reddit.top(time_filter='year', limit=1):
        print('Scanning:', submission.title, 'ID:', submission.id)

        '''collects hot comments from them'''
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print('[', comment.author, ']:', comment.body)
            comments_list.append(comment)

            comment_queue = submission.comments
