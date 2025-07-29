import yaml
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path: str = "config.yml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from YAML file or create interactive config."""
        if self.config_path.exists():
            with open(self.config_path, 'r') as file:
                return yaml.safe_load(file)
        else:
            return self._create_interactive_config()

    def _create_interactive_config(self) -> dict:
        """Create configuration interactively with user input."""
        config = {
            'exchange': input("Enter exchange name (e.g., 'binance'): "),
            'symbol': input("Enter trading pair (e.g., 'BTC/USDT'): "),
            'timeframe': input("Enter timeframe (e.g., '1h'): "),
            'mode': input("Enter mode (real-time/backtest): "),
            'strategy': {
                'name': input("Enter strategy name (e.g., 'RsiStrategy'): "),
                'params': {}
            },
            'api_keys': {
                'api_key': input("Enter API key: "),
                'secret_key': input("Enter secret key: ")
            }
        }

        # Save the config
        with open(self.config_path, 'w') as file:
            yaml.dump(config, file)

        return config

    def get_config(self) -> dict:
        """Get the current configuration."""
        return self.config
