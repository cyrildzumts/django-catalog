from django import template
from cart.cart_service import CartService


register = template.Library()


@register.simple_tag
def cart_box(request):
    context = {}
    if request.user.is_authenticated():
        cart = CartService.get_cart(request.user)
        count = CartService.items_count(cart.id)
        cartItems = cart.get_items()
    else:
        count = 0
        cartItems = None
    context = {'count' : count,
               'cartItems' : cartItems
            }
    return context
