from django import template
from catalog.models import Category, Product
# import datetime

register = template.Library()


@register.simple_tag
def subcategory(category=None):
    """
    @DEPRECATED
    Category Model Class now implement this method. 
    By default this method returns the direct 
    root children categories.
    if category is not None then this method
    return the subcategory of category

    """
    return Category.objects.filter(parent=category)


@register.simple_tag
def products_from_cat(category):
    """
    This method returns all the product from a 
    given category.
    """
    return Product.objects.filter(parent=category).order_by('-created_at')


@register.simple_tag
def get_default_products():
    """
     This Template Tag is used by index.html to 
     display the products shown on the home page.
     This used as a temporarly fix. This Tag would be deleted
     when the home page content would be properly defined.
    """
    return Product.objects.all()[:9]

@register.simple_tag
def banners():
    """
        This Template Tag is used to provide the products which
        appear in the site Banner.
        This used as a temporarly fix. This Tag would be deleted
        when the Banner content would be properly defined.
    """
    return Product.objects.all()[:5]