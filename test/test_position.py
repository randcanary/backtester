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

def test_decrease_position_partial():
    """Test selling part of a position and updating realized PnL."""
    position = Position(entry_price=50, quantity=100)
    position.decrease_position(sell_quantity=40, sell_price=55)

    assert position.quantity == 60  # 100 - 40 = 60 shares remaining
    assert position.current_price == 55
    assert position.get_realized_pnl() == (55 - 50) * 40  # Profit on 40 shares
    assert position.status == "open"  # Position should still be open

def test_decrease_position_fully():
    """Test selling all shares and closing the position."""
    position = Position(entry_price=50, quantity=100)
    position.decrease_position(sell_quantity=100, sell_price=55)

    assert position.quantity == 0  # All shares sold
    assert position.get_realized_pnl() == (55 - 50) * 100  # Profit on all shares
    assert position.status == "closed"  # Position should now be closed

def test_decrease_position_too_much():
    """Test selling more shares than available should raise an error."""
    position = Position(entry_price=50, quantity=100)

    with pytest.raises(ValueError, match="Cannot sell more than the current position size"):
        position.decrease_position(sell_quantity=150, sell_price=55)  # More than available

