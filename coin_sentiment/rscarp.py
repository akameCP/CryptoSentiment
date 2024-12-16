 # web scarping
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio
import nest_asyncio
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nest_asyncio.apply()

class NewsData():
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.text_crynews=''
        self.text_reddit=''
        
    
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
        
        content_reddit = soup_reddit.find_all(class_='absolute inset-0')
        content_reddit_last10 = content_reddit[-10:]
        for items_reddit in content_reddit_last10:
            self.text_reddit += (items_reddit.get_text(separator=' ',strip=True) + '\n'+'\n')
        
        content_crynews = soup_crynews.find_all(class_='post-loop__link')
        content_crynews_last10 = content_crynews [-10:]
        for items in content_crynews_last10:
            self.text_crynews += (items.get_text(separator=' ',strip=True)+'\n'+'\n')
        
        print(self.text_crynews)
        
        
        stat_reddit = float(self.sia.polarity_scores(self.text_reddit)['compound'])
        stat_crynews = float(self.sia.polarity_scores(self.text_crynews)['compound'])
        stat_reddit_pos = float(self.sia.polarity_scores(self.text_reddit)['pos'])
        stat_crynews_pos = float(self.sia.polarity_scores(self.text_crynews)['pos'])
        stat_reddit_neu = float(self.sia.polarity_scores(self.text_reddit)['neu'])
        stat_crynews_neu = float(self.sia.polarity_scores(self.text_crynews)['neu'])
        stat_reddit_neg = float(self.sia.polarity_scores(self.text_reddit)['neg'])
        stat_crynews_neg = float(self.sia.polarity_scores(self.text_crynews)['neg'])
        
        
        #print(text_reddit,text_crynews)
        #print(stat_reddit , stat_crynews)
        #print(stat_crynews)
        
        return ((stat_crynews + stat_reddit)/2), ((stat_crynews_pos + stat_reddit_pos)/2), ((stat_crynews_neu + stat_reddit_neu)/2), ((stat_crynews_neg + stat_reddit_neg)/2), ('reddit = '+self.text_reddit+'cry_news = '+self.text_crynews)
        
            
    def run(self):
        return asyncio.run(self.main())        


#news_data = NewsData()
#news_data.run()




