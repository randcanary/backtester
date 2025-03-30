

class Position:

    def __init__(self, entry_price, quantity, stop_loss = None, take_profit = None):
        """
        Initializes the Librarian class. 
        """
        self.mean_price = entry_price
        self.current_price = entry_price
        self.quantity = quantity
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.status = "open"  # "open" or "closed"
        self.realized_pnl = 0


    def update_price(self, price):
        """Updates the latest market price."""
        self.current_price = price

    def increase_position(self, current_price, quantity, stop_loss = None, take_profit = None):

        self.mean_price = (self.mean_price*self.quantity + current_price*quantity) / (self.quantity + quantity)

        self.current_price = current_price
        self.quantity += quantity
        
        self.stop_loss = stop_loss
        self.take_profit = take_profit
    
    def decrease_position(self, sell_quantity, sell_price, stop_loss = None, take_profit = None):

        if self.quantity < sell_quantity:
            raise ValueError("Cannot sell more than the current position size")
        
        self.quantity -= sell_quantity
        self.realized_pnl += sell_quantity * (sell_price - self.mean_price)
        self.current_price = sell_price

        self.stop_loss = stop_loss
        self.take_profit = take_profit

        if self.quantity == 0:
            self.status = "closed"


    def get_unrealized_pnl(self):
        """Calculates unrealized profit/loss if the position were closed now."""
        return (self.current_price - self.mean_price) * self.quantity
    
    def get_realized_pnl(self):
        """Calculates realized profit/loss if the position were closed now."""
        return self.realized_pnl

    
    def check_stop_take_profit(self, high_of_day, low_of_day):
        """Checks if stop-loss or take-profit has been hit."""
        if self.status == "closed":
            return None, None  # No need to check

        if self.stop_loss is not None and low_of_day <= self.stop_loss:
            return "stop_loss", self.stop_loss  # Close at stop-loss price
        if self.take_profit is not None and high_of_day >= self.take_profit:
            return "take_profit", self.take_profit  # Close at take-profit price

        return None, None  # No exit triggered
    
    def close_position(self, price):
        """Closes the position and calculates realized PnL."""
        if self.status == "closed":
            return  # Already closed

        self.realized_pnl += (price - self.mean_price) * self.quantity
        self.status = "closed"
    
