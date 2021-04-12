import redis
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
import json
from collections.abc import MutableMapping

r = redis.Redis()
r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})

print(r.get("Bahamas"))
print(uuid.uuid4())


def setflat_skeys(
        r: redis.Redis,
        obj: dict,
        prefix: str,
        delim: str = ":",
        *,
        _autopfix=""
) -> None:
    """Flatten `obj` and set resulting field-value pairs into `r`.

    Calls `.set()` to write to Redis instance inplace and returns None.

    `prefix` is an optional str that prefixes all keys.
    `delim` is the delimiter that separates the joined, flattened keys.
    `_autopfix` is used in recursive calls to created de-nested keys.

    The deepest-nested keys must be str, bytes, float, or int.
    Otherwise a TypeError is raised.
    """
    allowed_vtypes = (str, bytes, float, int)
    for key, value in obj.items():
        key = _autopfix + key
        if isinstance(value, allowed_vtypes):
            print(f"{prefix}{delim}{key} === {value}")
            r.set(f"{prefix}{delim}{key}", value)
        elif isinstance(value, MutableMapping):
            setflat_skeys(
                r, value, prefix, delim, _autopfix=f"{key}{delim}"
            )
        else:
            raise TypeError(f"Unsupported value type: {type(value)}")


@dataclass
class Customer:
    first_name: str
    last_name: str
    login: str


@dataclass
class Item:
    order_id: int
    name: str


class OrderStatus(Enum):
    IN_PROGRESS = "in_progress"
    WAITING_FOR_PAYMENT = "waiting_fot_payment"
    PAID = "paid"
    CANCELED = "canceled"


# https://redis.io/commands/hrandfield

order1 = {
    "order_id": str(uuid.uuid4()),
    **asdict(Customer("John", "Dou", "john_dou")),
    "items": json.dumps([
        asdict(Item(1, "Iphone")),
        asdict(Item(2, "TV samsung")),
        asdict(Item(3, "TV LG")),
        asdict(Item(4, "PlayStation")),
    ]),
    "total_price": 1000,
    "status": OrderStatus.IN_PROGRESS.value
}
order2 = {
    "order_id": str(uuid.uuid4()),
    **asdict(Customer("John", "Dou", "john_dou")),
    "items": json.dumps([
        asdict(Item(1, "Iphone")),
        asdict(Item(2, "TV samsung")),
        asdict(Item(3, "TV LG")),
        asdict(Item(4, "PlayStation")),
    ]),
    "total_price": 1000,
    "status": OrderStatus.WAITING_FOR_PAYMENT.value
}
setflat_skeys(r, order1, "1")
setflat_skeys(r, order2, "2")
# r.sadd(**order)
print(r.get("1:items"))
print(r.get("1:status"))
# print(r.hgetall(OrderStatus.IN_PROGRESS.value))
cursor, keys = r.scan(match='*status')
data = r.mget(keys)
print(data)
r.flushdb()
