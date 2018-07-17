from django.shortcuts import render
from catalog.models import Category, Product
from django.core import urlresolvers  # , serializers
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
# from django.template import RequestContext
from cart.cart_service import CartService
from cart.forms import ProductAddToCartForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from demosite import settings
from django.views.generic import DetailView, ListView
import calendar
from django.db.models import Q, F
import operator
from functools import reduce
from catalog.category_service import CategoryService
# Create your views here.

# this function return a list of subcategory
# which are parts of a parent category
# if parent category is zero, then  we are looking
# for the root category.


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_details_flat.html"
    #context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        p = super(ProductDetailView, self).get_object()
        name = p.name
        self.get_queryset().update(view_count=F('view_count') + 1)
        context['page_title'] = name + " | " + settings.SITE_NAME
        return context


class CategoryView(ListView):
    template_name = "catalog/category.html"
    paginate_by = 1

    def get_queryset(self):
        key = 'category_slug'
        self.category = get_object_or_404(Category, slug=self.kwargs[key])
        return self.category.children.all()

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        meta_keywords = self.category.meta_keywords
        meta_description = self.category.meta_description
        brands = set()
        print("Categoryview processin  products ...")
        products = CategoryService.get_products(self.category.id)
        print("Categoryview processin parent cats ...")
        parent_cats = CategoryService.get_parents_from(self.category.id)
        print("Categoryview processin root cats ...")
        root_cats = Category.objects.filter(parent=None)
        print("Categoryview processin brands ...")
        brands = CategoryService.get_brands(self.category.id)
        print("Categoryview processing done ...")
        context = {
            'root_cats'         : root_cats,
            'current_category'  : self.category,
            'parent_cats'       : parent_cats,
            'page_title'        : self.category.name + ' | ' + settings.SITE_NAME,
            'meta_keywords'     : meta_keywords,
            'meta_description'  : meta_description,
            'products'          : products,
            'brands'            : sorted(brands),
        }
        return context

    



def get_categories(parent_id):
    id = int(parent_id)
    return {'categories': Category.objects.filter(parent=id)}


def index(request):
    """
        This method serves the home page of the site.
        They are template tags already defined to provide
        by default context data containing the list of products
        to be displayed. See category_tags.py

    """
    template_name = "catalog/index_flat.html"
    # template_name = "base_flat.html"
    page_title = 'Acceuille | ' + settings.SITE_NAME
    current_cat = Category.objects.filter(parent=None)
    try:
        session = request.session
    # get the number of visits to the site
        if request.session.get('last_visit'):
            last_visit_time = session.get('last_visit')
            visits = session.get('visits', 0)
            delta = (datetime.now()-datetime.strptime(last_visit_time[:-7],
                 "%Y-%m-%d %H:%M:%S")
                 ).seconds
            if delta > 10:
                session['visits'] = visits + 1
                session['last_visit'] = str(datetime.now())
            else:
                session['last_visit'] = str(datetime.now())
                session['visits'] = 1
    except AttributeError:
        pass
    context = {'page_title': page_title,
               'current_category': current_cat,
            }
    return render(request, template_name, context)


def show_category(request, category_slug):
    """
        This method serves the Category page. 
        It renders the  page with products fromthe desired 
        category.
        @category_slug  is used the detect the desired the category.
        @request contains the page number used by a paginator

    """
    c = get_object_or_404(Category, slug=category_slug)
    # c.view_count = c.view_count + 1
    # c.save()
    template_name = "catalog/category.html"
    product_list = c.get_products()
    page_title = c.name + ' | ' + settings.SITE_NAME
    # show 9 product per page
    paginator = Paginator(product_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # page is not a not a number,
        # deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # if page is out of range (eg. 9999),
        # deliver the last page of results
        products = paginator.page(paginator.num_pages)
    meta_keywords = c.meta_keywords
    meta_description = c.meta_description
    context = {
        'current_category': c,
        'page_title': page_title,
        'meta_keywords': meta_keywords,
        'meta_description': meta_description,
        'products': products,
    }
    return render(request, template_name, context)


# product with POST and GET detection
def show_product(request, product_slug, template_name="catalog/product.html"):
    """
        This method displays the Product's information.
        The product is found using the slug attribut.
        This function will be update to query the product based on the 
        product ID.
        It possible for the user to add the displayed product into the cart,
        because of that we have to check whether the user used the GET or POST 
        HTTP method.
        If the user used GET then we just display the product details.
        If the user used POST then if want to add that product into the cart,
        we have to retrieve the product attribut that has been sent through
        a form, get the product and add it into the cart and return a json response.

        For static raison , we are counting the number of time this product
        has been displayed.

        As of now,the product page is served by the Class Based View ProductDetailView(defined above)
    """
    p = get_object_or_404(Product, slug=product_slug)
    categories = p.categories.filter(is_active=True)
    p.view_count = p.view_count + 1
    p.save()
    page_title = p.name + ' | ' + settings.SITE_NAME
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    # HTTP methods evaluation:
    if request.method == 'POST':
        # add to cart. create the bound form
        postdata = request.POST.copy()
        form = ProductAddToCartForm(request, postdata)
        # check if the postdata is valid
        if form.is_valid():
            # action = postdata.get('action')
            print("Add to Cart form is Valid")
            # add to cart and redirect to cart page
            user_cart = CartService.get_user_cart(request)
            # get product slug from postdata, return blank if empty
            product_slug = postdata.get('product_slug')
            # get quantity added, return 1 if empty
            quantity = postdata.get('quantity', 1)

            p = get_object_or_404(Product, slug=product_slug)
            # TO-DO Check if the product was added into the Cart
            user_cart.add_to_cart(product=p, quantity=int(quantity))
            # return JsonResponse({'status': 'ok'})
            # if test cookie worked, get rid of it

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            url = urlresolvers.reverse('cart:show_cart')
            return HttpResponseRedirect(url)

        else:
            #print("Add to Cart form is inValid")
            return JsonResponse({'status': 'error'})
    else:
        form = ProductAddToCartForm(request=request, label_suffix=':')
    # assign the hidden input the product_slug
    form.fields['product_slug'].widget.attrs['value'] = product_slug
    # set the test cookie on our first GET
    request.session.set_test_cookie()
    return render(request, template_name, locals())



def flyer(request):
    template_name = "catalog/flyer.html"
    page_title = 'Flyer Demo | ' + settings.SITE_NAME
    session = request.session
    # get the number of visits to the site

    if request.session.get('last_visit'):
        last_visit_time = session.get('last_visit')
        visits = session.get('visits', 0)
        delta = (datetime.now()-datetime.strptime(last_visit_time[:-7],
                 "%Y-%m-%d %H:%M:%S")
                 ).seconds
        if delta > 10:
            session['visits'] = visits + 1
            session['last_visit'] = str(datetime.now())
    else:
        session['last_visit'] = str(datetime.now())
        session['visits'] = 1
    return render(request, template_name, locals())


def search_view(request):
    """
        This function process the query emited by the user.
        It processes it by looking for Product with attributes 
        that match a defined filter : 
        *name
        *brand
        *Categories meta keyword
        *Meta keyword
    """
    template_name = "catalog/search_results.html"
    page_title = 'Resultats de la Recherche | ' + settings.SITE_NAME
    results = Product.objects.all()
    query = request.GET.get('search')
    query_list = query.split()
    count = len(query_list)
    if(count  > 0):
        results = results.filter(reduce(operator.or_, (Q(name__icontains=q) for q in query_list))|
                                 reduce(operator.or_, (Q(brand__icontains=q) for q in query_list))|
                                 reduce(operator.or_, (Q(categories__meta_keywords__icontains=q) for q in query_list))|
                                 reduce(operator.or_, (Q(meta_keywords__icontains=q) for q in query_list))
        )
    else:
        results = None
    context = {
        'page_title': page_title,
        'results' : results,
    }
    return render(request, template_name,context)
