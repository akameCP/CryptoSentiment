 # web scarping
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import time
import nest_asyncio
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nest_asyncio.apply()

class NewsData():
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    async def fetch(self,url):
        # create HTTP session
        async with aiohttp.ClientSession() as session:
            # make GET request using session
            async with session.get(url) as response:
                # return text content
                return await response.text()
            
    async def main(self):
        
        url1 = 'https://www.reddit.com/r/CryptoCurrency/new/'
        url2 = 'https://crypto.news/tag/bitcoin/'
        requests_reddit, requests_crynews = await asyncio.gather(self.fetch(url1),self.fetch(url2)) 
        soup_reddit = BeautifulSoup(requests_reddit, 'html.parser')
        soup_crynews = BeautifulSoup(requests_crynews, 'html.parser')
        content_reddit = soup_reddit.find(class_='absolute inset-0')
        content_crynews = soup_crynews.find(class_='post-loop__link')
        text_reddit =content_reddit.get_text(separator=' ',strip=True)
        text_crynews =content_crynews.get_text(separator=' ',strip=True)
        
        stat_reddit = float(self.sia.polarity_scores(text_reddit)['compound'])
        stat_crynews = float(self.sia.polarity_scores(text_crynews)['compound'])
        stat_reddit_pos = float(self.sia.polarity_scores(text_reddit)['pos'])
        stat_crynews_pos = float(self.sia.polarity_scores(text_crynews)['pos'])
        stat_reddit_neu = float(self.sia.polarity_scores(text_reddit)['neu'])
        stat_crynews_neu = float(self.sia.polarity_scores(text_crynews)['neu'])
        stat_reddit_neg = float(self.sia.polarity_scores(text_reddit)['neg'])
        stat_crynews_neg = float(self.sia.polarity_scores(text_crynews)['neg'])
        
        
        #print(text_reddit,text_crynews)
        #print(stat_reddit , stat_crynews)
        #print(stat_crynews)
        
        return ((stat_crynews + stat_reddit)/2), ((stat_crynews_pos + stat_reddit_pos)/2), ((stat_crynews_neu + stat_reddit_neu)/2), ((stat_crynews_neg + stat_reddit_neg)/2), (text_reddit+'\n'+text_crynews)
        
            
    def run(self):
        return asyncio.run(self.main())        


#news_data = NewsData()
#news_data.run()











