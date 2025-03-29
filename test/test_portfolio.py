import pytest
from position import Position
from portfolio import Portfolio

def test_initial_cash():
    portfolio = Portfolio(initial_cash=10000)
    assert portfolio.getCash() == 10000

def test_buy_success():
    portfolio = Portfolio(initial_cash=10000)
    assert portfolio.buy("AAPL", 100, 10, "2024-03-29")  # Buy 10 shares at $100
    assert portfolio.getCash() == 9000  # Cash should decrease
    assert "AAPL" in portfolio.positions

def test_buy_insufficient_cash():
    portfolio = Portfolio(initial_cash=500)
    assert not portfolio.buy("AAPL", 100, 10, "2024-03-29")  # Should fail due to low cash
    assert portfolio.getCash() == 500  # Cash should remain the same

def test_sell_success():
    portfolio = Portfolio(initial_cash=10000)
    portfolio.buy("AAPL", 100, 10, "2024-03-29")  # Buy first
    assert portfolio.sell("AAPL", 120, "2024-03-30")  # Sell at $120
    assert portfolio.getCash() == 10200  # Profit should be added
    assert "AAPL" not in portfolio.positions

def test_sell_without_position():
    portfolio = Portfolio(initial_cash=10000)
    assert not portfolio.sell("AAPL", 120, "2024-03-30")  # Should fail since no position exists
    assert portfolio.getCash() == 10000  # Cash should remain unchanged

def test_stop_loss():
    portfolio = Portfolio(initial_cash=10000)
    portfolio.buy("AAPL", 100, 10, "2024-03-29", stop_loss=95)
    portfolio.update_market("AAPL", high_of_day=105, low_of_day=94, latest_price=94, date="2024-03-30")
    assert "AAPL" not in portfolio.positions  # Position should be closed
    assert portfolio.getCash() == 9950  # Loss applied

def test_take_profit():
    portfolio = Portfolio(initial_cash=10000)
    portfolio.buy("AAPL", 100, 10, "2024-03-29", take_profit=110)
    portfolio.update_market("AAPL", high_of_day=111, low_of_day=98, latest_price=111, date="2024-03-30")
    assert "AAPL" not in portfolio.positions  # Position should be closed
    assert portfolio.getCash() == 10100  # Profit applied

def test_stop_loss_priority_over_take_profit():
    portfolio = Portfolio(initial_cash=10000)
    portfolio.buy("AAPL", 100, 10, "2024-03-29", stop_loss=95, take_profit=110)
    portfolio.update_market("AAPL", high_of_day=111, low_of_day=94, latest_price=111, date="2024-03-30")
    assert "AAPL" not in portfolio.positions  # Position should be closed
    assert portfolio.getCash() == 9950  # Stop loss took priority over take profit

def test_get_total_equity():
    portfolio = Portfolio(initial_cash=10000)
    portfolio.buy("AAPL", 100, 10, "2024-03-29")
    assert portfolio.get_total_equity() == 10000  # No change as market price == entry price
    portfolio.update_market("AAPL", high_of_day=105, low_of_day=95, latest_price=110, date="2024-03-30")
    assert portfolio.get_total_equity() == 10100  # Price increase reflected in equity
