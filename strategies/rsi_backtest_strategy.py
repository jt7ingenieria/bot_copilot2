from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd

class RsiBacktestStrategy(Strategy):
    # Define parameters that se pueden modificar desde la configuración
    rsi_period = 7  # Período más corto para más sensibilidad
    rsi_overbought = 60  # Ajustado para más señales
    rsi_oversold = 40    # Ajustado para más señales

    def init(self):
        # Calculate RSI using simple math
        self.rsi = self.I(self._calculate_rsi, self.data.Close, self.rsi_period)
        
    def _calculate_rsi(self, data, period):
        changes = pd.Series([data[i] - data[i-1] for i in range(1, len(data))])
        changes = pd.concat([pd.Series([0]), changes])  # Add 0 at the beginning
        
        gains = changes.copy()
        losses = changes.copy()
        gains[gains < 0] = 0
        losses[losses > 0] = 0
        losses = -losses
        
        avg_gains = self.I(lambda x: x.rolling(period).mean(), gains)
        avg_losses = self.I(lambda x: x.rolling(period).mean(), losses)
        
        rs = avg_gains / avg_losses
        return 100 - (100 / (1 + rs))
        
    def next(self):
        if len(self.rsi) < 2:  # Need at least 2 values to compare
            return
            
        current_rsi = self.rsi[-1]
        prev_rsi = self.rsi[-2]
        
        # Buy when RSI crosses up through oversold
        if prev_rsi <= self.rsi_oversold and current_rsi > self.rsi_oversold:
            if not self.position:  # Only buy if we don't have a position
                self.buy()
                
        # Sell when RSI crosses up through overbought
        elif prev_rsi <= self.rsi_overbought and current_rsi > self.rsi_overbought:
            if self.position:  # Only sell if we have a position
                self.sell()
