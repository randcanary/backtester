from portfolio import Portfolio
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class Backtest:
    def __init__(self, data, initial_cash=10000):
        self.portfolio = Portfolio(initial_cash)
        self.data = data

    def run(self):
        short_ma = self.data['Close'].rolling(window=5).mean()  # 5-day moving average

        for i in range(5, len(self.data)):
            date = self.data.index[i]
            close_price = self.data['Close'][i]
            high_of_day = self.data['High'][i]
            low_of_day = self.data['Low'][i]

            # Example strategy: Buy when price crosses above 5-day MA
            if close_price > short_ma[i] and 'STOCK' not in self.portfolio.positions:
                quantity = 10
                self.portfolio.buy('STOCK', close_price, quantity=quantity, date=date, stop_loss=close_price * 0.97, take_profit=close_price * 1.10)
            
            # Update existing positions and check stop-loss/take-profit
            self.portfolio.update_market('STOCK', high_of_day, low_of_day, close_price, date)
        
        print("Final Portfolio Value:", self.portfolio.get_total_equity())
        #self.portfolio.log_trades()

        self.plot_trades(self.data, self.portfolio.trades)

    def plot_trades(self, data, trades):
        """Plots stock price with buy/sell signals."""
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label='Stock Price', color='blue')
        
        buys = [(date, price) for date, price, action in trades if action == 'buy']
        sells = [(date, price) for date, price, action in trades if action == 'sell']
        
        if buys:
            buy_dates, buy_prices = zip(*buys)
            plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', s=100)
        
        if sells:
            sell_dates, sell_prices = zip(*sells)
            plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', s=100)
        
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Stock Price with Buy/Sell Signals')
        plt.legend()
        plt.show()
