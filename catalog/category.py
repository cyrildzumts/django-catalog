# from django.db import models
from catalog.models import Category, Product


class CategoryEntry:
    def __init__(self, category):
        self.current = category
        self.children = self.current.get_categories

    def is_parent(self):
        return self.children is not None

    def products(self):
        return Product.objects.filter()


class CategoryTree(object):
    pass


def has_children(category):
    return Category.objects.filter(parent=category) is None


def get_children_categories(category, cat_list=[]):
    if has_children(category):
        cat_list.append()
