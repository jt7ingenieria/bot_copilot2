# Cryptocurrency Trading Bot

This is a modular cryptocurrency trading bot implemented in Python. The bot supports both real-time trading and backtesting modes, with a Streamlit-based dashboard for visualization.

## Features

- Modular architecture for easy customization
- Real-time and backtesting modes
- Multiple technical indicators support
- Risk management and position sizing
- Interactive dashboard with Streamlit
- Asynchronous operation for better performance

## Project Structure

```
bot_copilot2/
├── config.yml                 # Configuration file
├── main.py                   # Main entry point
├── config_manager.py         # Configuration management
├── data_fetcher.py          # Data acquisition
├── indicator_calculator.py   # Technical indicators
├── data_preprocessor.py     # Data preprocessing
├── order_executor.py        # Order execution
├── backtester.py           # Backtesting engine
├── dashboard.py            # Streamlit dashboard
└── strategies/             # Trading strategies
    ├── base_strategy.py    # Base strategy class
    └── rsi_strategy.py     # RSI strategy implementation
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.yml` to set up your:
- Exchange credentials
- Trading pair
- Timeframe
- Strategy parameters
- Mode (real-time/backtest)

## Usage

1. For real-time trading:
   ```
   python main.py
   ```

2. For the dashboard:
   ```
   streamlit run dashboard.py
   ```

## Available Strategies

Currently implemented:
- RSI Strategy (Relative Strength Index)

To add a new strategy:
1. Create a new file in the `strategies` folder
2. Inherit from `BaseStrategy`
3. Implement the `generate_signal` method

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
