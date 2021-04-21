"""
Author: Shashank Nagaraja
Warning - This program contains functions from previous submissions to different classes. All code used is 
my own, but may have been written for another purpose and repurposed here. 
"""

#%%
import os
import pandas as pd
from tqdm import tqdm
import emoji
import nltk
from nltk.tokenize import TweetTokenizer
import re
import pickle

DATA_PATH = './data-extended'

#%%
def tweets_to_df(path_to_data):
    """Convert a list of json paths into one combined Pandas Dataframe using padnas read_json, This function is quite slow,
    there is probably a faster way to read json. 

    Args:
        path_to_data (string): Relative path to folder containing all the JSONs. Will look for ALL files
        ending with '.json'.

    Returns:
        pd.Dataframe: A Pandas Dataframe object with all 
    """
    finaldf = pd.DataFrame()
    for file in tqdm(os.listdir(path_to_data)):
        if file.endswith('.json'):
            # print(os.path.join(path_to_data, file))
            df = pd.read_json(os.path.join(path_to_data, file), lines = True)
            finaldf = finaldf.append(df)
    return finaldf

def clean_text(text_series, emoji_toText=False):
    """Clean tweet text with the following steps: (1)Remove Emojis and optionally convert to text 
    (2)Remove mentions (3)Remove URLs (4)Append item to cleaned text

    Args:
        text_series (Series): Series of tweets to clean. 
        emoji_toText (bool, optional): A boolean representing whether to add in text of correspoding emoji when
        it is removed. Defaults to False.

    Returns:
        Series: Series of strings with cleaned tweets.
    """
    cleaned_text = []
    for item in tqdm(text_series):
        # Remove capitalization
        item = item.lower()
        if (emoji_toText):
            # Remove Emojis, replace with text
            item = emoji.demojize(item, delimiters=(' ', ''))
        # Remove mentions
        item = re.sub('@[^\s]+', '', item)
        # Remove URLs
        item = re.sub(r"http\S+", '', item)
        if (item=='nan'):
            cleaned_text.append('')
        else: 
            # Append itme to cleaned text
            cleaned_text.append(item)    
    return cleaned_text

def tokenize_posts(text_series):
    """Tokenize using NLTKs TweetTokenizer.

    Args:
        text_series (Series): Series of strings representing tweets to tokenize. 

    Returns:
        List: List of lists where each sub-list represents a tokenized tweet. 
    """
    #print('\nTokenizing text\n')
    tokenizer = TweetTokenizer()
    tokens = []
    for post in tqdm(text_series):
        tokens.append(tokenizer.tokenize(post))
    return tokens

def main():
    # data = tweets_to_df(DATA_PATH)
    clean = clean_text(data['tweet'])
    mytoks = tokenize_posts(clean)
    
    return mytoks, data

# %%
if __name__ == '__main__':
    my_tokens, my_data = main()
    # Lets save progress here so that I don't have to run this again
    # Save Tokens 
    with open('./data-extended/my_tokens.pkl', 'wb') as f:
        pickle.dump(my_tokens, f)
    # Save DataFrame with all the tweets and metadata
    my_data.to_csv('./data-extended/tweets_df.csv')
# %%
