

class collect_sub:

    import praw
    from login_credentials import Login
    lg = Login()
    # login information for Reddit account is hidden in a gitignore file.
    # See 'login_template.py' for formatting guidelines
    reddit = praw.Reddit(client_id=lg.get_client_id,
                        client_secret=lg.get_client_secret,
                        password=lg.get_password,
                        user_agent=lg.get_user_agent,
                        username=lg.get_username)

    the_self = reddit.user.me()
    print('Hi! This is', the_self, 'an imma bout da scrape some philosophical scalps.')
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

    # print(comments_list)
