import datetime
from django.db import connection
from .models import Category, Product



class CategoryService():
    """
    This Class proposes it services to manage Category.
    It allow the client to get differents information
    on a Category.
    """




    @staticmethod
    def get_single_path(start, end, depth="t3"):
        query = "SELECT t1.id , t1.name as lev1 ,t1.slug as link1 , t2.id as id2, t2.name as lev2, t2.slug as link2,t3.id as id3, t3.name as lev3, t3.slug as link3, t4.id as id4, t4.name as lev4, t4.slug as link4 \
        FROM categories AS t1 LEFT JOIN categories AS t2 ON t2.parent_id = t1.id \
        LEFT JOIN categories AS t3 ON t3.parent_id = t2.id LEFT JOIN categories AS t4 \
        ON t4.parent_id = t3.id WHERE t1.name = '{0}' AND {1}.name = '{2}'".format(start, depth, end)

        row = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()[0]

        return row

    @staticmethod
    def get_path(start, end):
        row = None
        query = "SELECT end_cat.name as c_end, lev1.name as lev1, lev2.name as lev2, lev3.name as lev3, lev4.name as lev4 \
            FROM categories AS t1 , categories as end_cat \
            LEFT JOIN categories as lev1 on lev1.id = end_cat.parent_id \
            LEFT JOIN categories as lev2 on lev2.id = lev1.parent_id \
            LEFT JOIN categories as lev3 on lev3.id = lev2.parent_id \
            LEFT JOIN categories as lev4 on lev4.id = lev3.parent_id \
            WHERE t1.name =%s and  end_cat.name=%s"
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [start, end])
            row = cursor.fetchone()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Categoryservice : get_path() processing time : {0} ms".format(elapsed_time.microseconds / 1000))

        return row

    @staticmethod
    def get_leaf_nodes():
        query = "SELECT t1.* FROM categories AS t1 LEFT JOIN categories as t2 \
        ON t1.id = t2.parent_id WHERE t2.id IS NULL"
        return Category.objects.raw(query)


    @staticmethod
    def get_full_tree(start):
        rows = None
        query = "SELECT t1.id, t1.name, t1.slug, t2.id, t2.name, t2.slug,t3.id, t3.name, t3.slug , t4.id, t4.name, t4.slug \
            FROM categories AS t1 \
            LEFT JOIN categories AS t2 ON t2.parent_id = t1.id \
            LEFT JOIN categories AS t3 ON t3.parent_id = t2.id \
            LEFT JOIN categories AS t4 ON t4.parent_id = t3.id \
            WHERE t1.name =%s"
        with connection.cursor() as cursor:
            cursor.execute(query, [start])
            rows = cursor.fetchall()

        return rows
    
    @staticmethod
    def is_root_child(category, product_id):
        flag = False
        row = None
        #print("Category Check : {0}".format(category))
        if category:
            
            with connection.cursor() as cursor:

                query = "SELECT DISTINCT p.name , pc.category_id, t1.name as root_cat  from Product as p, Product_categories as pc, categories as root \
                    LEFT JOIN categories as t1 on t1.parent_id is NULL \
                    LEFT JOIN categories as t2 on t2.parent_id = t1.id \
                    LEFT JOIN categories as t3 on t3.parent_id = t2.id \
                    LEFT JOIN categories as t4 on t4.parent_id = t3.id \
                    WHERE p.id = pc.product_id and pc.category_id = root.id and p.id = %s \
                    and root.parent_id in ( t4.id ,t3.id ,t2.id ,t1.id)"
                start_time = datetime.datetime.now()
                cursor.execute(query,[product_id])
                row = cursor.fetchall()
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                print("Categoryservice : is_root_child() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
                if (row and len(row)):
                    row = row[0]
                    flag = category in row

        return  flag


    @staticmethod
    def get_parents_from(category_id):
        row = None
        paths = None
        query = "SELECT t1.id, t1.name, t1.slug, t2.id, t2.name, t2.slug,t3.id, t3.name, t3.slug , t4.id, t4.name, t4.slug \
            FROM categories AS t1 , categories as cat_end \
            LEFT JOIN categories AS t2 ON t2.parent_id = t1.id \
            LEFT JOIN categories AS t3 ON t3.parent_id = t2.id \
            LEFT JOIN categories AS t4 ON t4.parent_id = t3.id \
			WHERE t1.parent_id is NULL and cat_end.id=%s and cat_end.id in (t2.id, t3.id, t4.id)"
        print("Categoryservice : get_parent_from() cat id : {0}".format(category_id))
        with connection.cursor() as cursor:
            start_time = datetime.datetime.now()
            cursor.execute(query, [category_id])
            row = cursor.fetchall()
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            print("Categoryservice : get_parent_from() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
            if(row and len(row)):
                paths = list(zip(*[iter(row[0])]*3))
            else:
                print("CategoryService get_parents_from() no result")

        print("Categoryservice : paths processed")
        return paths


    @staticmethod
    def get_products(category_id):
        query= "SELECT  p.* from Product as p \
            LEFT JOIN Product_categories as pc on p.id=pc.product_id \
            LEFT JOIN categories as cat on cat.id=pc.category_id \
            LEFT JOIN categories as lev1 \
            LEFT JOIN categories as lev2 on lev2.parent_id=lev1.id \
            LEFT JOIN categories as lev3 on lev3.parent_id=lev2.id \
            LEFT JOIN categories as lev4 on lev4.parent_id=lev3.id \
            where cat.id in (lev1.id, lev2.id, lev3.id, lev4.id) and lev1.id= %s"
        start_time = datetime.datetime.now()
        queryset = Product.objects.raw(query, [category_id])
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("CategoryService get_products() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        return queryset


    @staticmethod
    def get_brands(category_id):
        start_time = datetime.datetime.now()
        queryset = CategoryService.get_products(category_id)
        brands = set()
        for p in queryset:
            brands.add(p.brand)
    
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print("CategoryService get_brand() processing time : {0} ms".format(elapsed_time.microseconds / 1000))
        return brands

def test_query():
    path = CategoryService.get_single_path('Mode', 'Talons', 't3')
    print("Model fields names:")
    for name in path.columns:
        print(name, end=' ')
    print(end='\n')
    return path

def test_query2():
    loafer = Product.objects.get(id=1)
    mode = Category.objects.get(name="Mode")
    smartphone = Category.objects.get(name="Smartphone")
    flag1 = mode.is_root_child(loafer)
    flag2 =  CategoryService.is_root_child(mode.name, loafer.id)
    cat = loafer.categories.all().first()
    products_1 = smartphone.get_products()
    products_2 = CategoryService.get_products(smartphone.id)
    brands = CategoryService.get_brands(smartphone.id)
    for brand in brands:
        print(brand)

    parent_cats = CategoryService.get_parents_from(cat.id)
