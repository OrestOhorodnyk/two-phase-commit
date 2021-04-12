from OrderManager import OrderManager
from orders import ORDERS
from OrderStatus import OrderStatus

order_manager = OrderManager()


def populate_redis():
    for order in ORDERS:
        order_manager.setflat_skeys(order, f"order:{order.get('order_id')}")


if __name__ == "__main__":
    populate_redis()
    print("Всі замовдення: ")
    order_manager.print_all_orders()
    print("*" * 200 + "\n")

    print("Замовлення по Id")
    order = order_manager.get_order_by_id(order_id=3)
    print(order)
    print("*" * 200 + "\n")

    print("Всі ідентифікатори замовлення статус яких Waiting for payment")
    waiting_for_payment = order_manager.get_order_id_by_status(OrderStatus.WAITING_FOR_PAYMENT)
    print(waiting_for_payment)
    print("*" * 200 + "\n")

    print("Всі ідентифікатори замовлення певного замовника")
    orders_by_login = order_manager.get_order_ids_by_login("jack_richer")
    print(orders_by_login)
    print("*" * 200 + "\n")

    print("Всі ідентифікатори замовлення певного замовника з можливістю вказати статус для пошуку")
    paid_orders = order_manager.get_order_ids_by_login_and_order_status("jack_richer", OrderStatus.PAID)
    print(paid_orders)
    print("*" * 200 + "\n")

    # можна не вказувати статус
    orders = order_manager.get_order_ids_by_login_and_order_status("jack_richer")


    order_manager.close_redis()
