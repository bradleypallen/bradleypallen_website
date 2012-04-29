import sys, re, optparse, tweepy, pymongo

def iso8601_timestamp(status):
    match = re.match('(\d\d\d\d-\d\d-\d\d) (\d\d:\d\d:\d\d)', str(status.created_at))
    return "%sT%sZ" % (match.group(1), match.group(2))

def iso8601_date(status):
    match = re.match('(\d\d\d\d-\d\d-\d\d)', str(status.created_at))
    return match.group(1)

def domain(url):
    match = re.match('http://([\w\-\.]+)/?', url)
    return match.group(1)

class API(tweepy.API):

    user_timeline = tweepy.binder.bind_api(
        path = '/statuses/user_timeline.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'include_entities', 'screen_name'],
        require_auth = True
    )

    retweeted_by_me = tweepy.binder.bind_api(
        path = '/statuses/retweeted_by_me.json',
        payload_type = 'status', payload_list = True,
        allowed_param = ['since_id', 'max_id', 'count', 'page', 'include_entities'],
        require_auth = True
    )

if __name__ == "__main__":
    
    # Specify and parse command lines arguments
    parser = optparse.OptionParser()
    parser.add_option('--screenname', action="store", dest="screen_name", default="bradleypallen", help="Twitter screen name")
    parser.add_option('--ckey', action="store", dest="consumer_key", default=None, help="Twitter consumer key")
    parser.add_option('--csecret', action="store", dest="consumer_secret", default=None, help="Twitter consumer secret")
    parser.add_option('--okey', action="store", dest="oauth_token_key", default=None, help="OAuth token key")
    parser.add_option('--osecret', action="store", dest="oauth_token_secret", default=None, help="OAuth token secret")
    parser.add_option('--dbhost', action="store", dest="dbhost", default="localhost", help="Database host")
    parser.add_option('--dbport', action="store", dest="dbport", default="27017", type=int, help="Database port")
    parser.add_option('--dbuser', action="store", dest="dbuser", default=None, help="Database account username")
    parser.add_option('--dbpassword', action="store", dest="dbpassword", default=None, help="Database account password")
    (options, args) = parser.parse_args()
    
    # Establish MongoDB database connection
    conn = pymongo.Connection(host=options.dbhost, port=options.dbport)
    db = conn.pageback
    db.authenticate(options.dbuser, options.dbpassword)
    statuses = db.statuses

    # Establish OAuth'd Tweepy session
    auth = tweepy.OAuthHandler(options.consumer_key, options.consumer_secret)
    auth.set_access_token(options.oauth_token_key, options.oauth_token_secret)
    api = API(auth)

    # Get id of most recent status
    since_id = db.statuses.find().sort('_id', pymongo.DESCENDING)[0]['_id']
    print 'Retrieving statuses since', since_id

    # Get statuses
    new_statuses = [ {'_id': status.id,
                      'account': options.screen_name,
                      'service': 'twitter',
                      'date': iso8601_timestamp(status), 
                      'day': iso8601_date(status), 
                      'body': status.text,
                      'tag': [ tag['text'] for tag in status.entities['hashtags'] ], 
                      'site': [ domain(link['url']) for link in status.entities['urls'] ], 
                      'friend': [ user['screen_name'] for user in status.entities['user_mentions'] ] } 
                     for status in tweepy.Cursor(api.user_timeline, since_id=since_id, include_entities=1, screen_name=options.screen_name).items() 
                   ]
    new_retweets = [ {'_id': status.id,
                      'account': options.screen_name,
                      'service': 'twitter',
                      'date': iso8601_timestamp(status), 
                      'day': iso8601_date(status), 
                      'body': status.text,
                      'tag': [ tag['text'] for tag in status.entities['hashtags'] ], 
                      # 'site': [ domain(link['url']) for link in status.entities['urls'] ], 
                      'friend': [ user['screen_name'] for user in status.entities['user_mentions'] ] } 
                     for status in tweepy.Cursor(api.retweeted_by_me, since_id=since_id, include_entities=1).items() 
                   ]

    # Insert statuses into MongoDB database
    statuses.ensure_index([ ("date", pymongo.ASCENDING), ("tag", pymongo.ASCENDING) ], unique=True)
    if len(new_statuses) > 0:
        print 'Inserting', len(new_statuses), 'new statuses...'
        statuses.insert(new_statuses)
    else:
        print 'No new statuses'
    if len(new_retweets) > 0:
        print 'Inserting', len(new_retweets), 'new retweets...'
        statuses.insert(new_retweets)
    else:
        print 'No new retweets'
    
