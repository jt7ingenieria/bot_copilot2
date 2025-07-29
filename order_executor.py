import ccxt.async_support as ccxt
from decimal import Decimal

class OrderExecutor:
    def __init__(self, exchange, config):
        self.exchange = exchange
        self.config = config
        self.position = None

    async def execute_trade(self, signal: int, last_price: float, balance: float):
        """
        Execute a trade based on the signal.
        
        Args:
            signal: 1 (buy), -1 (sell), 0 (hold)
            last_price: Current price of the asset
            balance: Available balance for trading
        """
        if signal == 0:
            return None

        try:
            # Calculate position size (1% of balance by default)
            risk_percentage = self.config.get('risk_percentage', 0.01)
            trade_amount_usd = balance * risk_percentage
            amount = self._calculate_amount(trade_amount_usd, last_price)

            # Determine order side
            side = 'buy' if signal == 1 else 'sell'

            # Set up stop loss and take profit
            sl_percentage = self.config.get('stop_loss_percentage', 0.02)  # 2% stop loss
            tp_percentage = self.config.get('take_profit_percentage', 0.05)  # 5% take profit

            stop_loss_price = self._calculate_stop_loss(last_price, side, sl_percentage)
            take_profit_price = self._calculate_take_profit(last_price, side, tp_percentage)

            # Create the order with stop loss and take profit
            order = await self._create_order(side, amount, last_price, stop_loss_price, take_profit_price)
            
            return order

        except Exception as e:
            print(f"Error executing trade: {e}")
            return None

    def _calculate_amount(self, trade_amount_usd: float, price: float) -> float:
        """Calculate the amount of asset to trade based on USD value."""
        amount = trade_amount_usd / price
        # Round to appropriate decimal places based on exchange minimums
        return float(Decimal(str(amount)).quantize(Decimal('0.00000001')))

    def _calculate_stop_loss(self, price: float, side: str, percentage: float) -> float:
        """Calculate stop loss price based on side and percentage."""
        multiplier = (1 - percentage) if side == 'buy' else (1 + percentage)
        return float(Decimal(str(price * multiplier)).quantize(Decimal('0.00000001')))

    def _calculate_take_profit(self, price: float, side: str, percentage: float) -> float:
        """Calculate take profit price based on side and percentage."""
        multiplier = (1 + percentage) if side == 'buy' else (1 - percentage)
        return float(Decimal(str(price * multiplier)).quantize(Decimal('0.00000001')))

    async def _create_order(self, side: str, amount: float, price: float, 
                          stop_loss_price: float, take_profit_price: float):
        """Create the main order with stop loss and take profit orders."""
        try:
            # Create the main market order
            params = {
                'stopLoss': {
                    'type': 'stopMarket',
                    'triggerPrice': stop_loss_price
                },
                'takeProfit': {
                    'type': 'takeProfitMarket',
                    'triggerPrice': take_profit_price
                }
            }

            order = await self.exchange.create_order(
                self.config['symbol'],
                'market',
                side,
                amount,
                None,  # Price is None for market orders
                params=params
            )

            print(f"Order executed: {side.upper()} {amount} {self.config['symbol']} @ market")
            print(f"Stop Loss: {stop_loss_price}")
            print(f"Take Profit: {take_profit_price}")

            return order

        except Exception as e:
            print(f"Error creating order: {e}")
            raise

    async def get_balance(self):
        """Get account balance."""
        try:
            balance = await self.exchange.fetch_balance()
            return balance
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None
