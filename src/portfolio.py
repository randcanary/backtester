from position import Position

class Portfolio:
    def __init__(self, initial_cash):
        self.cash = initial_cash  # Available cash balance
        self.positions = {}  # Active positions (key: stock, value: Position object)
        self.trade_log = []  # List of closed trades
        self.trades = []  # Store buy/sell signals for plotting

    def getCash(self):
        return self.cash

    def buy(self, stock, price, quantity, date, stop_loss=None, take_profit=None):
        """Buys a stock, opens a position, and updates cash."""
        cost = price * quantity
        if cost > self.cash:
            return False

        self.cash -= cost
        self.positions[stock] = Position(price, quantity, stop_loss, take_profit)
        self.trades.append((date, price, 'buy'))  # Store buy signal
        print(f"Buying at {price}, current balance is after buying is {self.cash}, total equity is {self.get_total_equity()}")
        return True

    def sell(self, stock, price, date):
        """Sells a stock, closes the position, and updates cash."""
        if stock not in self.positions:
            return False

        position = self.positions.pop(stock)
        position.update_price(price)
        position.close_position(price)
        self.cash += position.current_price*position.quantity # Add sale proceeds
        self.trade_log.append(position)
        self.trades.append((date, price, 'sell'))  # Store buy signal
        print(f"Selling at {price}, current balance is after selling is {self.cash}, total equity is {self.get_total_equity()}")
        return True

    def update_market(self, stock, high_of_day, low_of_day, latest_price, date):
        """Checks stop-loss/take-profit, updates price, and closes positions if needed."""
        if stock not in self.positions:
            return False

        position = self.positions[stock]
        trigger, exit_price = position.check_stop_take_profit(high_of_day, low_of_day)
        if trigger:
            self.sell(stock, exit_price, date)  # Auto-sell if SL/TP hit
        else:
            position.update_price(latest_price)

    def get_total_equity(self):
        """Returns total equity (cash + value of open positions)."""
        position_value = sum(pos.current_price * pos.quantity for pos in self.positions.values())
        return self.cash + position_value

    def log_trades(self):
        """Prints trade history."""
        for trade in self.trade_log:
            print(f"{trade.entry_price} -> {trade.realized_pnl:.2f} PnL")