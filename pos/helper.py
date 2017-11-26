from django.contrib.auth.models import User
from .models import Order, Cash, Order_Item


def setup_handling(request):
    cash, _ = Cash.objects.get_or_create(id=0)
    current_order = get_current_user_order(request.user.username)

    return (cash, current_order)


def get_current_user_order(username):
    usr = User.objects.get_by_natural_key(username)
    q = Order.objects.filter(user=usr, done=False)\
                     .order_by('last_change')
    if q.count() >= 1:
        return q[0]
    else:
        return Order.objects.create(user=usr)


def order_item_from_product(product, order):
    return Order_Item.objects.create(product=product,
                                     order=order,
                                     price=product.price,
                                     name=product.name)


def product_list_from_order(order):
    product_list = []
    order_item_list = Order_Item.objects.filter(order=order)

    for order_item in order_item_list:
        product_list.append(order_item.product)

    return product_list
