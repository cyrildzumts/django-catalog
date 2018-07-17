from catalog.models import Product, Category




class CatalogService:



    @staticmethod
    def update_product_price(product_id, price):
        Product.objects.filter(id=product_id).update(price=price)

    

    @staticmethod
    def apply_sale(sale, group):
        """
            Apply a sale on a group of products define 
            by group.
        """
        pass

    @staticmethod
    def remove_sale():
        pass
    
    @staticmethod
    def get_last_sold_product(limit):
        """
            This method returns the last sold products.
            The number of products returned is defined by the 
            parameter limit.
        """
        pass
    

    @staticmethod
    def get_total_product_in_store():
        """
         This method the current number of products
         available in the store.
         """
        return 0

    
    @staticmethod
    def check_availability(product_id):
        """
            This method checks whether a product is available.
            It returns the available quantity.
        """
        return 0