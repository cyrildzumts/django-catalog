from catalog.models import Category, Product
from catalog.category import CategoryEntry

# Global vairiable
VAR_CAT = None


class ParamItem:
    def __init__(self, cat, prod):
        self.category = cat
        self.product = prod

    def get_category(self):
        return self.category

    def get_product(self):
        return self.product

    def set_category(self, cat):
        self.category = cat

    def set_product(self, prod):
        self.product = prod


def print_products(entry):
    if entry:
        cat_name = entry.get_current().name
        products = entry.get_products()
        if products:
            print("Products from Category %s " % (cat_name))
            print("Category Url : %s" % (entry.get_current().get_absolute_url()))
            for p in products:
                print(p)
        else:
            print("Category %s has no products" % (cat_name))
    else:
        print("Entry is empty")


def test_query():
    root_list = list(Category.objects.filter(parent=None))
    for cat in root_list:
        # entry = CategoryEntry(cat)
        print(CategoryEntry(cat))

    print("Quitting query function.")


def is_root_child(product, category):
    current_cat = product.categories.get()
    while current_cat.parent is not None:
        current_cat = current_cat.parent
        if current_cat == category:
            return True
    return False


def get_products_from_cat(category, products):
    items = [p for p in products if is_root_child(p, category)]
    return items


def products_cat():

    all_cats = list(Category.objects.filter(parent=None))
    products = list(Product.objects.all())
    for c in all_cats:
        items = get_products_from_cat(c, products)
        if items is not None:
            print("-------------------------------------------------")
            print("children items from %s Category: " % (c.name))
            print("-------------------------------------------------")
            for p in items:
                print(p)
                print("Category Path : %s " % (p.cats_path))
        else:
            print("%s Category has no items " % (c.name))


def print_session():
    from django.contrib.sessions.models import Session
    sessions = Session.objects.all()
    if sessions:
        for s in sessions:
            print("session data : %s" % (s.session_data))
            print("session decoded data : ", end="")
            print(s.get_decoded())
    else:
        print("Sessions variable is empty")
