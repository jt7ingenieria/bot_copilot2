from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, params: dict):
        self.params = params

    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> int:
        """
        Generate a trading signal for the last data point.
        Returns: 1 (BUY), -1 (SELL), 0 (HOLD)
        """
        pass
