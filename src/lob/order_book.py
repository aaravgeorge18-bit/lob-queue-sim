from enum import Enum
from dataclasses import dataclass

class Side(Enum):
    BUY = "B"
    SELL = "S"

@dataclass
class Order:
    order_id: int
    price: int # in ticks; floats will cause rounding errors
    quantity: int
    side: Side