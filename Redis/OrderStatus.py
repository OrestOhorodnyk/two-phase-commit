from enum import Enum


class OrderStatus(Enum):
    IN_PROGRESS = "in_progress"
    WAITING_FOR_PAYMENT = "waiting_fot_payment"
    PAID = "paid"
    CANCELED = "canceled"
