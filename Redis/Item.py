from dataclasses import dataclass


@dataclass
class Item:
    order_id: int
    name: str
