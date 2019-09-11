from flask import Flask, escape, request, render_template
from dotenv import load_dotenv
import requests
import json
import os
load_dotenv()

app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    search_item = request.args.get('searchitem')
    tweets_json = get_tweets(search_item)
    tweets_dict_list = json.loads(tweets_json).get('statuses')
    if tweets_dict_list is None:
        tweets_dict_list = []
    return render_template('index.html', tweet_objs=tweets_dict_list)
    

def get_tweets(searchitem):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
    BEARER_TOKEN = os.getenv("BEARER_TOKEN") 
    headers = {'authorization': 'Bearer {}'.format(BEARER_TOKEN)}
    res = requests.get(url, headers=headers)
    return res.content

if __name__ == '__main__':
    app.run()