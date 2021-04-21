import twint
import pandas as pd 
# import time
from tqdm import tqdm

TOP_ACCOUNTS_FILE = 'Notable AI Accounts.csv'


top_ai_accs = pd.read_csv(TOP_ACCOUNTS_FILE)

def get_tweets(twitterhandles, tweetLimit):
    """
    This function takes in a list of twitter handles to scrape tweets from using TWINT (available at https://github.com/twintproject/twint). .
    Args:
        twitterhandles (list): List of twitter handles (strings) in the conventional twitter format of '@twitterhandle'. 
        tweetLimit (int): Maximum Number of tweets to scrape from each user supplied. 

    Returns:
        list: List of json objects that contains tweets from each handle in argument twitterhandles. 
    """
    tweets = []
    
    for handle in tqdm(twitterhandles):
        #print(f'Handle: {handle[1:]}')
        json_filename = f'./data-extended/{handle[1:]}-tweets.json'
        f = open(json_filename, 'w+')
        c = twint.Config()
        c.Username = handle[1:]
        c.Limit = tweetLimit
        c.Store_json = True
        c.Output = json_filename
        c.Hide_output = True
        # f'/data/{handle[1:]}-tweets.json'
        reply = twint.run.Search(c)
        tweets.append(reply)
        f.close()
    return tweets

def main():
    print("Attempting to Scrape Tweets for the following Twitter Handles:")
    print(top_ai_accs['Handle'])
    tweets = get_tweets(top_ai_accs['Handle'], 50)
    return tweets


if __name__ == "__main__":
    main()