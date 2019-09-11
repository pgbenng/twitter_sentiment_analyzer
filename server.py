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
    
    good_counter_and_bad_counter = []
    for tweet_dict in tweets_dict_list:
        counters = run_analysis(tweet_dict["text"])
        good_counter_and_bad_counter.append(counters)
    
    return render_template('index.html', tweet_objs=tweets_dict_list, answer=good_counter_and_bad_counter)

   
  



def get_tweets(searchitem):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
    BEARER_TOKEN = os.getenv("BEARER_TOKEN") 
    headers = {'authorization': 'Bearer {}'.format(BEARER_TOKEN)}
    res = requests.get(url, headers=headers)
    return res.content

def run_analysis(tweet_text):
    with open("positive.txt", "r") as f:
        positive_words = set(f.read().split("\n"))

    with open("negative.txt", "r") as f:
        negative_words = set(f.read().split("\n"))

    words = tweet_text.split(" ") 
    
    good_counter = 0
    bad_counter = 0
    for word in words:
        if word in positive_words:
            good_counter +=1
        if word in negative_words:
            bad_counter +=1
    ans = (good_counter, bad_counter)
    return ans
    
        
    


if __name__ == '__main__':
    app.run()