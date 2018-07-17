from django.db import models
from catalog import choices
from django.template.defaultfilters import slugify
import datetime
import time
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, help_text='Texte unique\
                            representant la page du produit.')
    # parent_category = models.IntegerField(default=0)
    parent = models.ForeignKey('self',blank=True,
                               null=True, related_name='children')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(max_length=255, help_text='Liste de mot clés,\
                                     séparés par une virgule,\
                                     utilisés pour la recherche')
    meta_description = models.CharField(max_length=255, help_text='Description\
                                        de mot clés')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'categories'
        ordering = ['name']
        verbose_name_plural = 'Categories'

    @property
    def categories(self):
        """
        Return a list of Categories path from the Root
        Category to the current Category(self).
        """
        cat_list = []
        current_cat = self
        while current_cat is not None:
            cat_list.append(current_cat)
            current_cat = current_cat.parent
        cat_list.reverse()
        return cat_list

    def subcategories(self):
        """
        This method returns the direct
        children categories.
        """
        #return Category.objects.filter(parent=self)
        return self.children.all()


    def root_cat(self):
        """
        When the current Category is a root Category,
        that is, self.parent is None , self is returned
        instead of None.
        """
        start_time = datetime.datetime.now()
        root = self
        while root.parent is not None:
            root = root.parent
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Cat root_cat() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        return root

    def is_root(self):
        """
        Return True if this is a root
        Category.
        """
        return self.parent is None

    def is_parent(self):
        """
        Return True if this Category is a parent
        Category.
        """
        return Category.objects.filter(parent=self).exists()

    def __str__(self):
        return self.name

    def is_root_child(self, product):
        """
        Return true if product belongs to the current
        Category or to a child of the current
        Category.
        """
        flag = False
        start_time = datetime.datetime.now()
        current_cat = product.categories.get()
        if current_cat == self:
            flag = True
        else:
            while current_cat.parent is not None:
                current_cat = current_cat.parent
                if current_cat == self:
                    flag = True
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Cat is_root_child() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        return flag

    def get_products(self):
        """
        Return every products which belong
        to this Category tree.
        """
        start_time = datetime.datetime.now()
        products = Product.objects.all().order_by('-created_at').filter()
        items = [p for p in products if self.is_root_child(p)]

        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("Cat get_products() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        return items

    def get_direct_products(self):
        """
        Return only products belonging
        to this Category
        """
        return self.product_set.all()

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:catalog_category', (), {'category_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class BaseProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    slug = models.SlugField(max_length=255, unique=True, help_text='Texte unique\
                            representant la page du produit.')
    price = models.IntegerField()
    old_price = models.IntegerField(default=0)
    sku = models.CharField(max_length=50)
    meta_keywords = models.CharField(max_length=255, help_text='Liste de mot clés,\
                                     séparés par une virgule,\
                                     utilisés pour la recherche')
    meta_description = models.CharField(max_length=255, help_text='Description\
                                        de mot clés')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    sell_quantity = models.IntegerField(default=0)
    sell_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to="products")
    is_available = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=True)

    class Meta:
        # abstract = True
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def build_slug(self):
        self.slug = self.name + "-" + self.id

    def build_sku(self):
        self.sku = self.brand + "-" + self.name

    @property
    def cats_path(self):
        return self.categories.get().categories

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:product_details', (), {'product_slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def product_is_available(self):
        return self.quantity != 0


class ProductType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    template_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # abstract = True
        db_table = 'ProductType'
        ordering = ['-created_at']

    def __str__(self):
        return self.type_name


class ModelNumber(models.Model):
    id = models.AutoField(primary_key=True)
    model_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ModelNumber'
        ordering = ['-created_at']


class Product(models.Model):
    TEMPLATE_NAME_CHOICES = (
        ('tags/product_phablet_options.html', 'Phablet'),
        ('tags/product_parfum_options.html', 'Parfum'),
        ('tags/product_shoe_options.html', 'Chaussure'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text='Texte unique representant la page du produit.',
        blank=True,
        null=False)
    size = models.CharField(max_length=5,
                            choices=choices.GENERIC_SIZE_CHOICES,
                            blank=True,
                            null=True)
    material = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=6,
                              choices=choices.GENDER_CHOICES,
                              blank=True,
                              null=True)
    categories = models.ManyToManyField(Category)
    price = models.IntegerField()
    old_price = models.IntegerField(default=0)
    model_number = models.ForeignKey(ModelNumber,
                                     related_name='product_model',
                                     unique=False,
                                     blank=True,
                                     null=True)
    meta_keywords = models.CharField(max_length=255, help_text='Liste de mot clés,\
                                     séparés par une virgule,\
                                     utilisés pour la recherche')
    meta_description = models.CharField(max_length=255, help_text='Description\
                                        de mot clés')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    short_description = models.TextField()
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    sell_quantity = models.IntegerField(default=0)
    sell_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to="products")
    image2 = models.ImageField(upload_to="products", blank=True, null=True)
    image3 = models.ImageField(upload_to="products", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=True)
    product_type = models.ForeignKey(ProductType,
                                     related_name='product_type',
                                     on_delete=models.CASCADE,
                                     unique=False)
    view_count = models.IntegerField(default=0)
    coupon = models.PositiveIntegerField(blank=True, null=True)
    template_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=TEMPLATE_NAME_CHOICES)

    class Meta:
        # abstract = True
        db_table = 'Product'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def build_slug(self):
        tmp = self.brand + "-" + self.name
        if self.slug != tmp:
            self.slug = tmp

    def build_sku(self):
        tmp = self.brand + "-" + self.name
        if self.sku != tmp:
            self.sku = self.brand + "-" + self.name

    @property
    def cats_path(self):
        return self.categories.get().categories

    @models.permalink
    def get_absolute_url(self):
        return ('catalog:product_details', (), {'slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def product_is_available(self):
        return (self.quantity > self.sell_quantity)

    def set_sell_quantity(self, quantity):
        if type(quantity) == int:

            if(quantity > 0 and quantity <= (self.quantity - self.sell_quantity)):
                self.sell_quantity = self.sell_quantity + quantity
                self.save()


    def save(self, *args, **kwargs):
        if(self.id is None):
            self.slug = slugify(self.name)
            self.build_sku()
        if(self.product_is_available() == False):
            self.is_available = False
        super(Product, self).save(*args, **kwargs)


    def is_recent(self):
        days = 14
        today = timezone.now()
        delta = datetime.timedelta(days = days)
        date = today - delta
        flag = self.created_at >= date
        return flag

    def get_color(self):
        colors = self.product_variants.values_list('color__name', flat=True).distinct()
        print("get color called")
        return colors

    def get_size(self, color_name=None):
        if color_name:
            colors = self.product_variants.filter(color__name=color_name).order_by('size__size').values_list('size__size', flat=True).distinct()
        else :
            colors = self.product_variants.order_by('size__size').values_list('size__size', flat=True).distinct()
        print("get size called with color_name : {}".format(color_name))
        return colors


class RelatedModel(models.Model):
    related_model = models.OneToOneField(
        BaseProduct,
        null=True,
        blank=True,
        related_name='product_details'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.related_model.name


class Phablet(Product):

    screen = models.FloatField(choices=choices.SCREEN_SIZE_CHOICES,
                               default=5)
    rear_camera = models.IntegerField(
        choices=choices.CAMERA_RESOLUTION_CHOICES,
        default=13,
        blank=True,
        null=True)
    front_camera = models.IntegerField(
        choices=choices.CAMERA_RESOLUTION_CHOICES,
        default=5,
        blank=True,
        null=True)
    system = models.CharField(max_length=512)
    memory = models.IntegerField(choices=choices.MEMORY_SIZE_CHOICES,
                                 default=16
                                 )
    ram_memory = models.IntegerField(default=1,
                                     choices=choices.RAM_SIZE_CHOICES)

    extern_sdcard = models.BooleanField(default=False)
    sim_card = models.CharField(
        choices=choices.SIM_CARD_CONF_CHOICES,
        default="STANDARD",
        max_length=15
        )
    battery = models.CharField(max_length=128)

    class Meta:
        db_table = 'phones'


class Parfum(Product):

    capacity = models.IntegerField(choices=choices.PARFUMS_QUANTITY_CHOICES,
                                   default=100)
    typ = models.CharField(max_length=10,
                           choices=choices.PARFUM_TYP_CHOICES,
                           default='EDP')

    class Meta:
        db_table = 'parfums'

    def build_sku(self):
        self.sku = self.brand + "-" + self.name + "-" + str(self.capacity)


class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=7, help_text="Valeur de la couleur\
     en hexadecimal")

    class Meta:
        db_table = 'colors'
        ordering = ['name']

    def __str__(self):
        return self.name + " : " + self.value



class Size(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.CharField(max_length=30)

    class Meta:
        db_table = 'sizes'
        ordering = ['size']

    def __str__(self):
        return "Size : {}".format(self.size)


class SizeProduct(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.ForeignKey(Size, related_name="sizes_product", unique=False)
    product = models.ForeignKey(Product, related_name="sizesproducts", unique=False)
    color = models.ForeignKey(Color, related_name="colors_sizeproduct", unique=False, blank=True, null=True)

    def __str__(self):
        return self.product.name + " : " + self.size.size



class ColorProduct(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.ForeignKey(Color, related_name="colors_product", unique=False)
    product = models.ForeignKey(Product, related_name="products", unique=False)
    size = models.ForeignKey(Size, related_name="sizes_colorproduct", unique=False,blank=True, null=True)

    def __str__(self):
        return self.product.name + " : " + self.color.value


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    def __str__(self):
        return "Product Variant : {}".format(self.name)


class VariantOption(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name="product_variants", unique=False, blank=True, null=True)
    product_variant = models.ForeignKey(ProductVariant, related_name="variants", unique=False, blank=True, null=True)
    sku = models.CharField(max_length=30, unique=True, null=False)
    color = models.ForeignKey(Color, related_name="color_variants", unique=False)
    price =  models.IntegerField(default=0)
    size = models.ForeignKey(Size, related_name="size_variants", unique=False,blank=True, null=True)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to="products", blank=True, null=True)
    image2 = models.ImageField(upload_to="products", blank=True, null=True)
    image3 = models.ImageField(upload_to="products", blank=True, null=True)
