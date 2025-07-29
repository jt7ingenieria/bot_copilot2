from backtesting import Backtest, Strategy
import pandas as pd

class BacktestingEngine:
    def __init__(self, data: pd.DataFrame, strategy_class, params: dict, 
                 initial_cash: float = 10000, commission: float = 0.001):
        """
        Initialize the backtesting engine.
        
        Args:
            data: DataFrame with OHLCV data and indicators
            strategy_class: The strategy class to test
            params: Strategy parameters
            initial_cash: Initial capital
            commission: Commission rate per trade (0.1% default)
        """
        self.data = data
        self.strategy_class = strategy_class
        self.params = params
        self.initial_cash = initial_cash
        self.commission = commission
        self.results = None

    def run(self):
        """
        Run the backtest and return the results.
        """
        # Create Backtest instance
        bt = Backtest(
            self.data,
            self.strategy_class,
            cash=self.initial_cash,
            commission=self.commission,
            exclusive_orders=True
        )

        # Run optimization if params is a dict of lists
        if any(isinstance(v, list) for v in self.params.values()):
            self.results = bt.optimize(**self.params)
        else:
            self.results = bt.run(**self.params)

        return self.results

    def get_performance_metrics(self):
        """
        Get key performance metrics from the backtest.
        """
        if self.results is None:
            raise ValueError("No backtest results available. Run the backtest first.")

        metrics = {
            'Return [%]': self.results['Return [%]'],
            'Buy & Hold Return [%]': self.results['Buy & Hold Return [%]'],
            'Max. Drawdown [%]': self.results['Max. Drawdown [%]'],
            'Sharpe Ratio': self.results['Sharpe Ratio'],
            'Sortino Ratio': self.results['Sortino Ratio'],
            'Calmar Ratio': self.results['Calmar Ratio'],
            'SQN': self.results['SQN'],
            'Trades': self.results['# Trades'],
            'Win Rate [%]': self.results['Win Rate [%]'],
            'Best Trade [%]': self.results['Best Trade [%]'],
            'Worst Trade [%]': self.results['Worst Trade [%]'],
            'Avg. Trade [%]': self.results['Avg. Trade [%]'],
            'Max. Trade Duration': self.results['Max. Trade Duration'],
            'Avg. Trade Duration': self.results['Avg. Trade Duration'],
        }

        return metrics

    def plot(self, filename=None):
        """
        Plot the backtest results.
        
        Args:
            filename: If provided, save the plot to this file
        """
        if self.results is None:
            raise ValueError("No backtest results available. Run the backtest first.")

        return self.results._trades.plot()
