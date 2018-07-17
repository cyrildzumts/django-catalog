from django import template
from django.utils import timezone
from catalog.models import Category, Phablet, Parfum, Product
import datetime
register = template.Library()

# a Cache variable to store Site Categories list
cat_set = Category.objects.all()
mode_cat = cat_set.get(name="Mode")
beauty_cat = cat_set.get(name="Beauté")
parfum_cat = cat_set.get(name="Parfumerie")
smartphone_cat = cat_set.get(name="Smartphone")


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    """
    This method returns a list of all the
    active categories.
    """
    active_categories = Category.objects.filter(is_active=True)
    return {
            'active_categories': active_categories,
            'request_path': request_path
            }


@register.inclusion_tag("tags/phone_list.html")
def phone_list():
    print("phone_list tags called.")
    return {'recent_phones': Phablet.objects.all()}


@register.inclusion_tag("tags/parfum_list.html")
def parfum_list():
    return {'recent_parfums': Parfum.objects.all()}


@register.simple_tag
def current_time(format_string=''):
    if format_string:
        return datetime.datetime.now().strftime(format_string)
    return datetime.datetime.now().strftime("%d / %m / %Y - %H : %M")


@register.simple_tag
def display_session(request):
    print("Request Scheme : %s " % (request.scheme))
    print("Request Method : %s " % (request.method))
    print("Request Path : %s " % (request.path))
    session = request.session
    print("Session Object: ")
    print("Session Expire Age : %d" % (session.get_expiry_age()))

    print("Session Content :")
    for k in session.keys():
        print("Key : %s" % (k))
    return request.session

@register.simple_tag
def root_categorie():
    """
    This method return the root categories
    """
    #print("roots cats called ")
    root_cats = Category.objects.filter(is_active=True, parent=None)
    return {'root_cats': root_cats}


@register.simple_tag
def get_home_items(group):
    """
    This method returns a list of items
    depending on the group value:
    group = 0 --> Newly added items
    group = 1 --> Parfums
    group = 2 --> Mode
    group = 4 --> Electronics
    group = 5 --> Sale
    group = 6 --> Random
    """
    queryset = Product.objects.all()
    items = None
    days = 700
    if group is not None:
        if group == 0:
            #print ("get New Items")
            today = timezone.now()
            delta = datetime.timedelta(days = days)
            date = today - delta
            items = queryset.filter(created_at__gt=date)
        if group == 1:
            items = queryset.filter(product_type=3)
        if group == 2:
            mode = Category.objects.all().get(name="Mode")
            items = mode.get_products()
        if group == 3:
            mode = Category.objects.all().get(name="Smartphone")
            items = mode.get_products()

    return items[:3]


@register.simple_tag
def get_cat(category):
    """
    This methode return the category model
    """
    cat = None
    if category is not None:
        if category == "Mode":
            cat = mode_cat
        elif category == "Parfumerie":
            cat = parfum_cat
        elif category == "Beauty":
            cat = beauty_cat
        elif category == "Smartphone":
            cat = smartphone_cat
    return cat

