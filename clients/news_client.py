import sys
import os
import json
from newsapi import NewsApiClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import NEWS_API_KEY
from src.styles import GREEN, RED, RESET

def fetchNews(ticker, sortMethod, fromTime, toTime):
    outputPath = 'datasets/news.json'
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    #All news within a given time frame, from all sources
    everything = newsapi.get_everything(
        q=ticker,
        language='en',
        sort_by=sortMethod,
        domains='biztoc.com',
        from_param=fromTime,
        to=toTime
    )

    #write to 'news.json'
    if everything:
        with open(outputPath, 'w') as json_file:
            json.dump(everything, json_file, indent=4)
            print(f"{GREEN}Data has been written to {outputPath}{RESET}")
    else:
        print(f"{RED}Error writing data to {outputPath}{RESET}")
