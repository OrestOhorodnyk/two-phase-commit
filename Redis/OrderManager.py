import redis
from collections.abc import MutableMapping

from OrderStatus import OrderStatus


class OrderManager:
    def __init__(self):
        self.r = redis.Redis(decode_responses=True)

    def setflat_skeys(self, obj: dict, prefix: str, delim: str = ":", *, _autopfix="") -> None:
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
                # print(f"key: {prefix}{delim}{key} value: {value}")
                self.r.set(f"{prefix}{delim}{key}", value)
            elif isinstance(value, MutableMapping):
                self.setflat_skeys(
                    self.r, value, prefix, delim, _autopfix=f"{key}{delim}"
                )
            else:
                raise TypeError(f"Unsupported value type: {type(value)}")

    def close_redis(self):
        self.r.close()

    def print_all_orders(self):
        for key in self.r.keys("order:*"):
            print(f'key: {key} value: {self.r.mget(key)}')

    def get_order_by_id(self, order_id: int) -> dict:
        res = {}
        for key in self.r.keys(f"order:{order_id}*"):
            res[key.split(':')[2]] = self.r.mget(key)[0]
        return res

    def get_order_id_by_status(self, status: OrderStatus) -> list[str]:
        order_id_list = []
        for key in self.r.keys(f"*status*"):
            if status.value == self.r.mget(key)[0]:
                order_id_list.append(":".join(key.split(":")[:2]))
        return order_id_list

    def get_order_ids_by_login(self, login: str) -> list[str]:
        order_id_list = []
        for key in self.r.keys(f"*login*"):
            if login == self.r.mget(key)[0]:
                order_id_list.append(":".join(key.split(":")[:2]))
        return order_id_list

    def get_order_ids_by_login_and_order_status(self, login: str, status: OrderStatus = None) -> list[str]:
        order_id_list = []
        for key in self.r.keys(f"*login*"):
            if login == self.r.mget(key)[0]:
                for s in self.r.keys(f"{':'.join(key.split(':')[:2])}:status"):
                    if status and status.value == self.r.mget(s)[0]:
                        order_id_list.append(":".join(key.split(":")[:2]))
                    if not status:
                        order_id_list.append(":".join(key.split(":")[:2]))
        return order_id_list
