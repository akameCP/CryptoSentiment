

import ccxt.async_support as ccxt
import numpy as np
import asyncio
import pandas as pd
import time
import matplotlib.pyplot as plt
import nest_asyncio

nest_asyncio.apply()

class BtcGraphData():
    def __init__ (self):
        
        self.symbol = 'BTC/USDT'
        self.timeframe = '1h'  # 1 saatlik zaman dilimi
        self.exchange = ccxt.binance()
        
    async def get_closing_prices(self):
        
        
        ohlcv = await self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=100)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        close_prices = df['close']
        high_prices = df['high']
        low_prices = df['low']
        open_prices = df['open']
        
        plt.plot(close_prices)
        plt.show()
        await self.exchange.close()
        
        return close_prices.values
        
    def run(self):
        return asyncio.run(self.get_closing_prices())        
    
    




    

if __name__ == "__main__":
    btc_graph_data = BtcGraphData()
    btc_graph_data.run()








































        
        
    
        
