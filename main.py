import asyncio
import pandas as pd
from config_manager import ConfigManager
from data_fetcher import DataFetcher
from indicator_calculator import calculate_indicators
from data_preprocessor import DataPreprocessor
from strategies.rsi_strategy import RsiStrategy
from order_executor import OrderExecutor
from backtester import BacktestingEngine
from dashboard import Dashboard

async def run_bot():
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.get_config()

    # Initialize components
    data_fetcher = DataFetcher(config)
    preprocessor = DataPreprocessor()
    strategy = RsiStrategy(config['strategy']['params'])
    order_executor = OrderExecutor(data_fetcher.exchange, config)

    if config['mode'] == 'backtest':
        await run_backtest(config, data_fetcher, preprocessor, strategy)
    else:
        await run_realtime(config, data_fetcher, preprocessor, strategy, order_executor)

async def run_backtest(config, data_fetcher, preprocessor, strategy):
    """Run backtesting mode."""
    print("Starting backtesting...")
    
    # Fetch historical data for a longer period
    data = await data_fetcher.fetch_historical_data('2023-01-01', '2024-07-01')
    
    # Calculate indicators
    data = calculate_indicators(data)
    
    # Preprocess data
    data = preprocessor.preprocess_data(data, ['rsi', 'volume'])
    
    # Import and run backtest with the specific backtesting strategy
    from strategies.ema_volume_strategy import EmaVolumeStrategy
    
    # Run backtest
    engine = BacktestingEngine(
        data=data,
        strategy_class=EmaVolumeStrategy,
        params={
            'ema_short': 9,
            'ema_medium': 21,
            'ema_long': 50,
            'volume_factor': 1.5,
            'volume_period': 20
        },
        initial_cash=100000,  # Capital inicial para BTC
        commission=0.001
    )
    
    results = engine.run()
    metrics = engine.get_performance_metrics()
    
    # Print backtest results
    print("\nBacktest Results:")
    print("-" * 50)
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print("-" * 50)

async def run_realtime(config, data_fetcher, preprocessor, strategy, order_executor):
    """Run real-time trading mode."""
    print("Starting real-time trading...")
    
    dashboard = Dashboard()
    
    async def process_new_data(data):
        """Process new data and execute trades."""
        # Calculate indicators
        data_with_indicators = calculate_indicators(data)
        
        # Preprocess data
        processed_data = preprocessor.preprocess_data(
            data_with_indicators, 
            ['rsi', 'volume']
        )
        
        # Generate trading signal
        signal = strategy.generate_signal(processed_data)
        
        if signal != 0:
            # Get current balance
            balance = await order_executor.get_balance()
            if balance:
                # Execute trade
                last_price = processed_data['close'].iloc[-1]
                await order_executor.execute_trade(
                    signal, 
                    last_price,
                    float(balance['total']['USDT'])
                )
        
        # Update dashboard
        dashboard.render(
            data=processed_data,
            balance=await order_executor.get_balance(),
            open_positions=None,  # Implement get_positions() in OrderExecutor
            trade_history=None    # Implement get_trade_history() in OrderExecutor
        )
    
    # Start real-time data feed
    await data_fetcher.start_realtime_feed(process_new_data)

if __name__ == "__main__":
    asyncio.run(run_bot())
