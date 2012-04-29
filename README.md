# A re-implementation of my personal web site in Node.js

## Requirements

### Web server

- express
- forever
- jade
- sass
- optimist
- mongodb

### Python worker

- Python >= 2.6
- tweepy
- pymongo
- optparse

## Running the web server

- $ forever start app.js --port {port} --dbhost {mongoHost} --dbport {mongoPort} --dbuser {user} --dbpassword {password}

## Running the Twitter lifestream daemon
- $ python update_lifestream.py --screenname={twitterScreenname} --ckey={twitterConsumerKey} --csecret={twitterConsumerSecret} --okey={oauthTokenKey} --osecret={oauthTokenSecret} --dbhost={mongoHost} --dbport={mongoPort} --dbuser={user} --dbpassword={password}

