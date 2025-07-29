import ccxt.async_support as ccxt
import pandas as pd
import asyncio
from tenacity import retry, stop_after_attempt, wait_fixed

class DataFetcher:
    def __init__(self, config: dict):
        self.exchange = getattr(ccxt, config['exchange'])({
            'apiKey': config['api_keys']['api_key'],
            'secret': config['api_keys']['secret_key'],
        })
        self.symbol = config['symbol']
        self.timeframe = config['timeframe']

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    async def fetch_ohlcv(self, since=None, limit=100):
        """
        Fetch OHLCV data from the exchange.
        """
        try:
            data = await self.exchange.fetch_ohlcv(
                self.symbol, 
                self.timeframe, 
                since=since, 
                limit=limit
            )
            df = pd.DataFrame(
                data, 
                columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df.set_index('timestamp')
            # Remove duplicate indices
            df = df[~df.index.duplicated(keep='first')]
            return df
        except Exception as e:
            print(f"Error fetching OHLCV data: {e}")
            raise
        finally:
            await self.exchange.close()

    async def fetch_historical_data(self, start_date, end_date=None):
        """
        Fetch historical data between start_date and end_date.
        """
        all_data = []
        current_since = int(pd.Timestamp(start_date).timestamp() * 1000)
        
        while True:
            chunk = await self.fetch_ohlcv(since=current_since, limit=1000)
            if chunk.empty:
                break
                
            all_data.append(chunk)
            if end_date and chunk.index[-1] >= pd.Timestamp(end_date):
                break
                
            current_since = int(chunk.index[-1].timestamp() * 1000)
            await asyncio.sleep(self.exchange.rateLimit / 1000)  # Respect rate limits
            
        if not all_data:
            return pd.DataFrame()
            
        # Concatenate all data and remove duplicates
        df = pd.concat(all_data)
        df = df[~df.index.duplicated(keep='first')]
        return df

    async def start_realtime_feed(self, callback):
        """
        Start a real-time data feed.
        """
        while True:
            try:
                data = await self.fetch_ohlcv(limit=1)
                if not data.empty:
                    await callback(data)
                await asyncio.sleep(int(self.timeframe[:-1]) * 60)  # Sleep based on timeframe
            except Exception as e:
                print(f"Error in real-time feed: {e}")
                await asyncio.sleep(5)  # Wait before retrying
