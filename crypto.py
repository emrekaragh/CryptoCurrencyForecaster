import tweepy
import requests
import pandas as pd
from datetime import datetime
from cryptocmd import CmcScraper


#credentials for twitter api
consumer_key="Rwv9mpaXLlNjyQTFjnj4yJwEa"
consumer_secret="iQ7m01ZO39YodfpofJnPVm4ko8aaY0iAeMu48cuF87rWc9VCER"
access_token="1062745141-R1nZIzHJyqYrvR2P3Y6QS8hn24tPTu0Ihxtoxxy"
access_token_secret="ipORa3Y5ezGMbQNkA3mFxlY47HyeWrK994z4AVLGTiil9"


cmc_key='a57df474-1dcc-44ea-9876-0e29392d850f'
nomic_key='f7aad6ca0c259aa07e992f676c1d03561c11eac6'

def get_fear_and_greed_index():
    url='https://api.alternative.me/fng/?limit=99999999'
    data = pd.json_normalize(requests.get(url).json().get('data'))
    data['timestamp']=data['timestamp'].apply(lambda x: datetime.fromtimestamp(int(x)))
    data['date']=data['timestamp'].dt.date
    data=data[data['date'].astype(str)<='2022-03-29']
    return data[['value','value_classification','date']]

def get_info(key):
    url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': key,
    }
    data=pd.json_normalize(requests.get(url, headers=headers).json().get('data'))
    return data

def get_dominance_nomic(key,currency_list):
    url="https://api.nomics.com/v1/currencies/ticker?key={}&ids={}&interval=1d,365d&per-page=100&page=1".format(nomic_key,','.join(currency_list))
    data=pd.json_normalize(requests.get(url).json())
    return data


def get_market_cap(currency_list):
    dates=pd.period_range(start='2017-01-01',end='2022-03-29',freq='D')
    
    df = pd.DataFrame(dates, columns=['Date'])
    df['Date']=pd.to_datetime(df['Date'].astype(str)).dt.date
    
    for i in currency_list:
        scraper = CmcScraper(i)
        temp_df = scraper.get_dataframe()
        temp_df['Date']=pd.to_datetime(temp_df['Date']).dt.date
        temp_df.rename({'Market Cap':'{}_market_cap'.format(i)},axis=1,inplace=True)
        df=df.merge(temp_df[['Date','{}_market_cap'.format(i)]],how='left',on='Date')
    return df


#%%
currency_list = ['BTC','AVAX','LUNA','ETH','DOT','MINA','DYDX','NEAR','ADA','USDT','SOL','BNB','ADA','XRP']

fear_and_greed_index=get_fear_and_greed_index()
cmc_info=get_info(cmc_key)
market_cap=get_market_cap(currency_list)

fear_and_greed_index.to_csv('./output/fear_and_greed_index.csv',index=False)
market_cap.to_csv('./output/market_cap.csv',index=False)
#cmc_info.to_csv('./output/cmc_info.csv',index=False)


"""
#%%
auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

test= api.search_tweets(q='BTC from:whale_alert')

tweets = api.user_timeline(screen_name='whale_alert', 
                       # 200 is the maximum allowed count
                       count=200,
                       include_rts = False,
                       # Necessary to keep full_text 
                       # otherwise only the first 140 words are extracted
                       tweet_mode = 'extended'
                       )
all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id
while True:
    tweets = api.user_timeline(screen_name='whale_alert', 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           max_id = oldest_id - 1,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    if len(tweets) == 0:
        break
    oldest_id = tweets[-1].id
    all_tweets.extend(tweets)
    print('N of tweets downloaded till now {}'.format(len(all_tweets)))
    
outtweets = [[tweet.id_str, 
              tweet.created_at, 
              tweet.favorite_count, 
              tweet.retweet_count, 
              tweet.full_text.encode("utf-8").decode("utf-8")] 
             for idx,tweet in enumerate(all_tweets)]
df = pd.DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count","text"])


key_str='unknown wallet to'
coin_list=['BTC','ETH']

df=df[(df['text'].str.contains(key_str))]
df=df[df['text'].str.contains('|'.join(coin_list))]
tweets=pd.DataFrame(df['created_at'].dt.date.unique(),columns=['date'])


import csv
alltweets = []	
screen_name='whale_alert'

auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)
	
#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = screen_name,count=200)

#save most recent tweets
alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1

#keep grabbing tweets until there are no tweets left to grab
while len(new_tweets) > 0:
	print("getting tweets before {}".format(oldest))
	
	#all subsiquent requests use the max_id param to prevent duplicates
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#update the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	print("...{} tweets downloaded so far".format(len(alltweets)))

#transform the tweepy tweets into a 2D array that will populate the csv	
outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
#%%
#write the csv	
with open('{}_tweets.csv'.format(screen_name), 'w') as f:
	writer = csv.writer(f)
	writer.writerow(["id","created_at","text"])
	writer.writerows(outtweets)
	print('{}_tweets.csv was successfully created.'.format(screen_name))
    
    
#%%
import tweepy as tw
api = tw.API(auth, wait_on_rate_limit=True)
consumer_key="Rwv9mpaXLlNjyQTFjnj4yJwEa"
consumer_secret="iQ7m01ZO39YodfpofJnPVm4ko8aaY0iAeMu48cuF87rWc9VCER"
access_token="1062745141-R1nZIzHJyqYrvR2P3Y6QS8hn24tPTu0Ihxtoxxy"
access_token_secret="ipORa3Y5ezGMbQNkA3mFxlY47HyeWrK994z4AVLGTiil9"


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

for tweets in api.search_tweets(q="iphone", lang="en"):
    print(tweets.text)

search_words = "btc"


tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="en").items(3500)
tweet_list= []
for tweet in tweets:
    tweet_list.append(tweet)
"""