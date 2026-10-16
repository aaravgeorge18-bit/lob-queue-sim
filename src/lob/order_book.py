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
    

class OrderBook:
    def __init__(self):
        self.bids = {} # price -> PriceLevel
        self.asks = {} # price -> PriceLevel

    def best_bid(self) -> int | None:
        if not self.bids:
            return None
        return max(self.bids)
    
    def best_ask(self) -> int | None:
        if not self.asks:
            return None
        return min(self.asks)
    
    def add_order(self, order):
        if order.side == Side.BUY:
            book = self.bids
        else:
            book = self.asks

        if order.price not in book:
            book[order.price] = PriceLevel(order.price)
        book[order.price].add(order)

