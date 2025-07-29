from .base_strategy import BaseStrategy
import pandas as pd

class RsiStrategy(BaseStrategy):
    def generate_signal(self, data: pd.DataFrame) -> int:
        """
        Generate trading signals based on RSI strategy.
        """
        if data.empty or 'rsi' not in data.columns:
            return 0
            
        latest_rsi = data['rsi'].iloc[-1]
        overbought = self.params.get('rsi_overbought', 70)
        oversold = self.params.get('rsi_oversold', 30)

        if latest_rsi > overbought:
            return -1  # Sell signal
        elif latest_rsi < oversold:
            return 1   # Buy signal
        else:
            return 0   # Hold
