import json
from dataclasses import asdict

from Customer import Customer
from Item import Item
from OrderStatus import OrderStatus

ORDERS = [{
    "order_id": 1,
    **asdict(Customer("John", "Dou", "john_dou")),
    "items": json.dumps([
        asdict(Item(1, "Iphone")),
        asdict(Item(2, "TV samsung")),
        asdict(Item(3, "TV LG")),
        asdict(Item(4, "PlayStation")),
    ]),
    "item_count": 4,
    "total_price": 1000,
    "status": OrderStatus.IN_PROGRESS.value
}, {
    "order_id": 2,
    **asdict(Customer("Jack", "Richer", "jack_richer")),
    "items": json.dumps([
        asdict(Item(1, "Samsung S21")),
        asdict(Item(2, "TV samsung")),
        asdict(Item(3, "TV LG")),
    ]),
    "item_count": 3,
    "total_price": 950,
    "status": OrderStatus.WAITING_FOR_PAYMENT.value
},
    {
        "order_id": 3,
        **asdict(Customer("Lee", "Hou", "lee_hou")),
        "items": json.dumps([
            asdict(Item(1, "xiaomi redmi note")),
            asdict(Item(2, "TV hitachi")),
        ]),
        "item_count": 2,
        "total_price": 300,
        "status": OrderStatus.PAID.value
    },
    {
        "order_id": 4,
        **asdict(Customer("Mary", "Smite", "mary111")),
        "items": json.dumps([
            asdict(Item(1, "item 1")),
            asdict(Item(2, "item 2")),
        ]),
        "item_count": 2,
        "total_price": 500,
        "status": OrderStatus.WAITING_FOR_PAYMENT.value
    },
    {
        "order_id": 5,
        **asdict(Customer("Jack", "Richer", "jack_richer")),
        "items": json.dumps([
            asdict(Item(1, "Item 1")),
            asdict(Item(2, "Item 2")),
        ]),
        "item_count": 2,
        "total_price": 350,
        "status": OrderStatus.PAID.value
    },

]
