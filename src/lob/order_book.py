from enum import Enum
from dataclasses import dataclass
from collections import deque

class Side(Enum):
    BUY = "B"
    SELL = "S"


@dataclass
class Order:
    order_id: int
    price: int # in ticks; floats will cause rounding errors
    quantity: int
    side: Side


class PriceLevel:
    def __init__(self, price: int):
        self.price = price
        self.orders = deque()  # oldest orders fill first
        self.total_qty = 0  # total quantity at this price level
    
    def add(self, order: Order):
        self.orders.append(order)
        self.total_qty += order.quantity