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
        fills = []
        if order.side == Side.BUY:
            book = self.bids
            opposite = self.asks
        else:
            book = self.asks
            opposite = self.bids
        
        while order.quantity > 0 and self.crosses(order):
            best_price = self.best_ask() if opposite is self.asks else self.best_bid()
            level = opposite[best_price]
            maker = level.orders[0]
            traded = min(order.quantity, maker.quantity)
            order.quantity -= traded
            maker.quantity -= traded
            level.total_qty -= traded
            fills.append(Fill(price= level.price, quantity= traded, maker_id= maker.order_id, 
            taker_id= order.order_id, taker_side= order.side))
            if maker.quantity == 0:
                level.orders.popleft()
            if not level.orders:
                del opposite[level.price]
        if order.quantity > 0:
            if order.price not in book:
                book[order.price] = PriceLevel(order.price)
            book[order.price].add(order)

        return fills

    def crosses(self, order):
        if order.side == Side.BUY:
            best_price = self.best_ask()
            if best_price is None:
                return False
            return order.price >= best_price
        else:
            best_price = self.best_bid()
            if best_price is None:
                return False
            return order.price <= best_price

@dataclass
class Fill:
    price: int
    quantity: int
    maker_id: int
    taker_id: int
    taker_side: Side
    
