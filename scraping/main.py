import time 
from datetime import datetime, timedelta
from Topic import Topic
import csv
from configparser import ConfigParser
from random import randint 
from twikit import Client, TooManyRequests
import asyncio

#------------------------------------Will Change---------------------------------------
MINIMUM_TWEETS = 20
client = Client(language='en-US')
now = datetime.now()
yesterday = now - timedelta(days=10)
since_date = yesterday.strftime('%Y-%m-%d')
until_date = now.strftime('%Y-%m-%d')
#--------------------------------------------------------------------------------------

async def get_tweets(tweets, url):        
    QUERY = f"from:{url} since:{since_date}"
    if tweets is None: 
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top') # does so in 20's so if wuery is 41 it will get 60
    else: 
        wait_time = randint(5,9)
        print(f'{datetime.now()} - Getting next teets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets


async def tweet_caller(name, url):
    #getting tweets to populate the CSV
    tweet_count = 0
    tweets = None    
    while tweet_count < MINIMUM_TWEETS: 
        try: 
            tweets = await get_tweets(tweets, url)       
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue
        if not tweets: 
            print(f'{datetime.now()} - No more tweets found')
            break
        for tweet in tweets: 
            tweet_count += 1
            tweet_data = [tweet.id, tweet.created_at, tweet.user.screen_name, tweet.user.profile_image_url, tweet.user.is_blue_verified, tweet.text, tweet.media, tweet.urls, tweet.thumbnail_url, tweet.favorite_count, tweet.view_count, tweet.retweet_count, ]
            with open(f"{name}_tweets.csv", 'a', newline='', encoding='utf-8') as file: 
                writer = csv.writer(file)
                writer.writerow(tweet_data)
    print(f'{datetime.now()} - Done! {tweet_count} tweets found')

async def sign_in():
    username = "ThrowawayLate"  
    password = "LaterThrowMeAway1!"

    email = "ThrowawayLater01@gmail.com" 
    formatted_date = now.strftime("%d%m%Y")
     # Client Authentication and cookie storage
    await client.login(auth_info_1=username, auth_info_2=email, password=password)  
    client.save_cookies(f'{formatted_date}.json')


async def main_request(name, urls, hashtags): 
    wait_time = randint(1,5)
    with open(f'{name}_tweets.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        writer.writerow(['id','created_at','screen_name','profile_img','verified','text','media', 'urls', 'thumbnail', 'favorite_count','view_count','retweet_count'])
    for url in urls:
        print(url)
        await asyncio.sleep(wait_time) 
        await tweet_caller(name, url)
    for hashtag in hashtags:
        print(hashtag)
        await asyncio.sleep(wait_time)
        await tweet_caller(name,hashtag)


def fetch_tweets(topics):
    asyncio.run(fetch_tweets_for_all(topics))


async def fetch_tweets_for_all(topics):
    firstRun = True
    for topic in topics:
        if firstRun:
            await sign_in()
            firstRun = False 
        print(f"Fetching tweets for topic: {topic.name}")
        await main_request(topic.name, topic.urls, topic.hashtags)


# NEEDS WORK: 100 ACCOUNTS, 10 HASHTAGS
hash_bio = ['#Biology', '#Genetics', '#Evolution', '#Ecology', '#Microbiology', '#Neuroscience', '#Botany', '#Zoology', '#Biodiversity', '#ClimateChange']
hash_news = ['#WorldNews', '#GlobalPolitics', '#BreakingNews', '#Economy', '#Conflict', '#Diplomacy', '#HumanRights', '#GlobalHealth', '#ClimateCrisis', '#Refugees']
hash_ai = ['#AI', '#MachineLearning', '#DeepLearning', '#NLP', '#Robotics', '#Automation', '#AIethics', '#ComputerVision', '#ReinforcementLearning', '#DataMining']
hash_math = ['#Mathematics', '#Algebra', '#Geometry', '#Calculus', '#Statistics', '#NumberTheory', '#MathEducation', '#DataScience', '#Puzzles', '#MathHistory']

topic_biology = Topic('Biology', [
  "@NatureNews", "@CellCellPress", "@ScienceMagazine", "@TheScientistLLC",
  "@PLOSBiology", "@eLife", "@NatureBiotech", "@GeneticsGSA", "@ASMicrobiology",
  "@ASCBiology", "@RoyalSocBio", "@BiochemSoc", "@MicrobioSoc", "@GeneticsSociety",
  "@BiophysicalSoc", "@SACNAS", "@AAAS", "@NIH", "@NSF", "@CDCgov", "@WHO",
  "@HHMINEWS", "@NCBI", "@EMBO", "@JAXGenomicMed", "@BroadInstitute", "@SangerInstitute",
  "@ColdSpringHarb", "@RockefellerUniv"],hash_bio) 
topic_ai = Topic('Artificial Intelligence', ['lexfridman', 'DeepMind', 'OpenAI', 'AndrewYNg', 'MIT_CSAIL'],hash_ai)
topic_math = Topic('Mathematics', ['Mathologer', 'standupmaths', 'fermatslibrary', 'stevenstrogatz', 'MathematicsProf'],hash_math)
topic_world_news = Topic('World News', ['BBCWorld', 'CNN', 'Reuters', 'AJEnglish', 'TheEconomist'],hash_news)
topics = [topic_biology]

# "@PLOSBiology", "@eLife", "@NatureBiotech", "@GeneticsGSA", "@ASMicrobiology",
#   "@ASCBiology", "@RoyalSocBio", "@BiochemSoc", "@MicrobioSoc", "@GeneticsSociety",
#   "@BiophysicalSoc", "@SACNAS", "@AAAS", "@NIH", "@NSF", "@CDCgov", "@WHO",
#   "@HHMINEWS", "@NCBI", "@EMBO", "@JAXGenomicMed", "@BroadInstitute", "@SangerInstitute",
#   "@ColdSpringHarb", "@RockefellerUniv"]


fetch_tweets(topics)


        

    
    
