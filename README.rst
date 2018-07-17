==========
Catalog
==========

Catalog is a Django app to provide a shopping Catalog facility to a
Django Website.
The Catalog presents diverse Models : Category, Product, ProductVariant,
VariantOption, Color, Size

For a detailed documentation please have a look in the "docs" directory.

Quick start :
-------------

1. Add "catalog" to your INSTALLED_APPS setting like this :
	INSTALLED_APPS = [
		...
		'catalog',

	]

2. Include the cart URLConf in your project urls.py like this :
	url(r'^', include('catalog.urls')),


3. Run 'python manage.py migrate' to create the  models needed by the Catalog.

4. Visit localhost:8000 to see the Catalog.
