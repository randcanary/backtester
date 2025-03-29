import pytest
from position import Position  # Adjust import path as needed

def test_initialization():
    pos = Position(entry_price=100, quantity=10, stop_loss=90, take_profit=110)
    assert pos.mean_price == 100
    assert pos.quantity == 10
    assert pos.stop_loss == 90
    assert pos.take_profit == 110
    assert pos.status == "open"
    assert pos.get_unrealized_pnl() == 0

def test_update_price():
    pos = Position(entry_price=100, quantity=10)
    pos.update_price(105)
    assert pos.current_price == 105
    assert pos.get_unrealized_pnl() == 50  # (105 - 100) * 10

def test_stop_loss_trigger():
    pos = Position(entry_price=100, quantity=10, stop_loss=95)
    trigger, price = pos.check_stop_take_profit(high_of_day=102, low_of_day=94)
    assert trigger == "stop_loss"
    assert price == 95

def test_take_profit_trigger():
    pos = Position(entry_price=100, quantity=10, take_profit=105)
    trigger, price = pos.check_stop_take_profit(high_of_day=106, low_of_day=99)
    assert trigger == "take_profit"
    assert price == 105

def test_close_position():
    pos = Position(entry_price=100, quantity=10)
    pos.close_position(110)  # Closing at 110
    assert pos.status == "closed"
    assert pos.get_realized_pnl() == 100  # (110 - 100) * 10

def test_no_double_close():
    pos = Position(entry_price=100, quantity=10)
    pos.close_position(110)
    first_pnl = pos.get_realized_pnl()
    pos.close_position(120)  # Attempt to close again
    second_pnl = pos.get_realized_pnl()
    assert first_pnl == second_pnl  # Ensure it doesn't change after the first close

def test_increase_position():
    pos = Position(entry_price=100, quantity=10, stop_loss=80, take_profit=100)
    pos.increase_position(current_price = 110, quantity=10, stop_loss=90, take_profit=110)
    assert pos.mean_price == 105
    assert pos.quantity == 20
    assert pos.stop_loss == 90
    assert pos.take_profit == 110
    pos.increase_position(current_price = 90, quantity = 10, stop_loss=80, take_profit=100)
    assert pos.mean_price == 100
    assert pos.quantity == 30
    assert pos.stop_loss == 80
    assert pos.take_profit == 100

