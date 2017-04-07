Installation instructions
-------------------------
- virtualenv (https://virtualenv.pypa.io/en/stable/installation/)

Unless you know well about managing your system wide installation and
versions (and even if you do), please have virtualenv installed and
setup.

- Python 3.5 / Python 2.7
- Django==1.10.3 (pip install django)
- djangorestframework==3.5.3

If you want to use Python 2.7, that's totally fine. Just make sure
Django works properly for your setup and have djangorestframework
installed.

We will use sqlite as the database, which usually comes bundled
along with Python. But just double check to make sure that you have it
installed. (Hint: Simply starting a Django project and running "python
manage.py migrate" should work flawlessly and leave you with a
db.sqlite3 file in your root folder).

Project Description
-------------------

A very basic inventory system with products and categories. We'll use
the following models:


class Category(models.Model):
    name = models.CharField(max_length=50)
    status = models.IntegerField(default=1)


class Stat(models.Model):
    category_count = models.IntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category)


A guide to following the steps below
------------------------------------

First of all, please keep http://www.cdrf.co/ open.

The bullet numbers below are actions that you have to do. Each bullet
point refers to the implementation of one part of the project.

The '*'s are API call examples. You have to make sure that each of
them return successfully before proceeding to the next line.

If you see an 'X' just below an '*', then the 'X' refers to an
expected error. Make sure you run into the exact same error before
proceeding.

The '-'s are line or chunks of code that you'll have to add into your
project at that point.

The 'O's are expected outputs of the immediately preceeding API calls
marked with a '*'.


1. Implement the Cateogry model and define the /categories/ endpoint.

 - class Category(models.Model):
       name = models.CharField(max_length=50)

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Fruits"}' "http://localhost:8000/api/v1/categories/"
 * curl -H "Content-Type:application/json" -X DELETE "http://localhost:8000/api/v1/categories/2/"
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/1/"
 * curl -H "Content-Type:application/json" -X PATCH -d '{"name":"Vegetables"}' "http://localhost:8000/api/v1/categories/1/"

2. Breakup the SimpleRouter entry for /categories/ and implement it manually.

 - url(r'^categories/$', CategoryViewSet, name='category-list')
 X {
    `Exception Type: TypeError
    Exception Value: __init__() takes exactly 1 argument (2 given)`
   }

 - url(r'^categories/$', CategoryViewSet.as_view(), name='category-list')
 X {
    `TypeError: The 'actions' argument must be provided when calling
    '.as_view()' on a ViewSet. For example '.as_view({'get': '
    list'})'`
   }

 - url(r'^categories/$', CategoryViewSet.as_view({'get':'list'}), name='category-list')

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Fruits"}' "http://localhost:8000/api/v1/categories/"
 X {"detail":"Method \"POST\" not allowed."}

 - url(r'^categories/$', CategoryViewSet.as_view({'get':'list', 'post':'create'}), name='category-list')

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Fruits"}' "http://localhost:8000/api/v1/categories/"
 * curl -H "Content-Type:application/json" -X DELETE "http://localhost:8000/api/v1/categories/3/"
 X Page not found (404)

 - url(r'^categories/(?P<pk>[0-9]+)/$', CategoryViewSet.as_view({'delete':'destroy'}), name='category-detail')

 * curl -H "Content-Type:application/json" -X DELETE "http://localhost:8000/api/v1/categories/3/"
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/1/"
 X {"detail":"Method \"GET\" not allowed."}

 - url(r'^categories/(?P<pk>[0-9]+)/$', CategoryViewSet.as_view({'get':'retrieve', 'delete':'destroy'}), name='category-detail')

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/1/"
 * curl -H "Content-Type:application/json" -X PATCH -d '{"name":"Meat"}' "http://localhost:8000/api/v1/categories/1/"
 X {"detail":"Method \"PATCH\" not allowed."}

 - url(r'^categories/(?P<pk>[0-9]+)/$', CategoryViewSet.as_view({'get':'retrieve', 'delete':'destroy', 'patch':'partial_update'}), name='category-detail')

 * curl -H "Content-Type:application/json" -X PATCH -d '{"name":"Meat"}' "http://localhost:8000/api/v1/categories/1/"

3. Create a Stat model and a /stats/ endpoint (Use ReadOnlyModelViewSet).

 - class Stat(models.Model):
       category_count = models.IntegerField()

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/stats/"

4. Update Stat whenever a Category is created. (Override `def create()`)

 - def create(self, request, *args, **kwargs):
       serializer = self.get_serializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       self.perform_create(serializer)
       if Stat.objects.exists():
           s = Stat.objects.get()
           s.category_count += 1
           s.save()
       else:
           Stat.objects.create(category_count=1)
       headers = self.get_success_headers(serializer.data)
       return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Crockery"}' "http://localhost:8000/api/v1/categories/"
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/stats/"
 O [{"id":1,"category_count":3}]

5. Update Stat whenever a Cateogry is deleted. (Override `def destroy()`).

 - def destroy(self, request, *args, **kwargs):
       instance = self.get_object()
       self.perform_destroy(instance)

       s = Stat.objects.get()
       s.category_count -= 1
       # This should never happen. The idea here is to just demonstrate overriding destroy().
       # if s.category_count < 1:
       #    s.category_count = 0
       s.save()

       return Response(status=status.HTTP_204_NO_CONTENT)

 * curl -H "Content-Type:application/json" -X DELETE "http://localhost:8000/api/v1/categories/5/"
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/stats/"
 O [{"id":1,"category_count":2}]

6. Add a `status` field to the Category model (You might have this
   field already implemented). In point 5 above, we are doing a hard
   delete of the category model. Instead, while overriding destroy(),
   you can probably just set the `status` field to 0, ie, a soft
   delete.

 - status = models.IntegerField(default=1)

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 O [{"id":1,"name":"Meat","status":1},{"id":4,"name":"Crockery","status":1},{"id":5,"name":"Cosmetics","status":1}]
 * curl -H "Content-Type:application/json" -X PATCH -d '{"status":0}' "http://localhost:8000/api/v1/categories/5/"
 O {"id":5,"name":"Cosmetics","status":0}
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 O [{"id":1,"name":"Meat","status":1},{"id":4,"name":"Crockery","status":1},{"id":5,"name":"Cosmetics","status":0}]

7. Only display categories with status 1. (Override `def get_queryset()`)

 - def get_queryset(self):
       queryset = Category.objects.filter(status=1)
       return queryset

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 O [{"id":1,"name":"Meat","status":1},{"id":4,"name":"Crockery","status":1}]

8. Create a Product model and a /products/ endpoint.
8.1. Add REST_FRAMEWORK = {'PAGE_SIZE':10} to settings.py

 - class Product(models.Model):
       name = models.CharField(max_length=50)
       category = models.ForeignKey(Category)

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 O [{"id":1,"name":"Meat","status":1},{"id":4,"name":"Crockery","status":1}]
 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Vessel", "category":4}' "http://localhost:8000/api/v1/products/"
 O {"id":1,"name":"Vessel","category":4}
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/products/"
 O {"count":1,"next":null,"previous":null,"results":[{"id":1,"name":"Vessel","category":4}]}

9. Hmm. `Category:4` doesn't tell us much. Let's make it tell us more about category itself. Let's edit the ProductSerializer 
 - class ProductSerializer(serializers.ModelSerializer):
       category = CategorySerializer()
       class Meta:
           model = Product

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/products/" | python -m json.tool
 O {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            },
            "name": "Vessel"
        }
    ]
   }

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Vessel", "category":4}' "http://localhost:8000/api/v1/products/"
 X {"category":{"non_field_errors":["Invalid data. Expected a dictionary, but got int."]}}

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Stove", "category":{"id":4,"name":"Crockery","status":1}}' "http://localhost:8000/api/v1/products/"
 X AssertionError: The `.create()` method does not support writable
   nested fields by default.  Write an explicit `.create()` method for
   serializer `products.serializers.ProductSerializer`, or set
   `read_only=True` on ne sted serializer fields.

10. Override the .create() method on the ProductSerializer. (We are
    not putting read_only=True because category is a required FK value for
    a product object to be created. You can try putting
    read_only=True. You will get a "IntegrityError: NOT NULL constraint
    failed" error)

 - def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(**category_data)
        product = Product.objects.create(category=category, **validated_data)
        return product

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Stove", "category":{"id":4,"name":"Crockery","status":1}}' "http://localhost:8000/api/v1/products/"
 O {"id":3,"category":{"id":4,"name":"Crockery","status":1},"name":"Stove"}

11. It is cumbersome to keep sending the entire JSON of an FK object
    whenever you want a new object to be created. So let's se e how we can
    fix that. Let's edit ProductSerializer. (Remember to comment out the
    overridden .create() method as we no longer need that)

 - class ProductSerializer(serializers.ModelSerializer):
       category_id = serializers.PrimaryKeyRelatedField(
            write_only=True,
	    queryset=Category.objects.all(),
            source='category'
       )
       category = CategorySerializer(read_only=True)

       class Meta:
            model = Product
            fields = ('id', 'name', 'category_id', 'category')

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Glass", "category_id":4}' "http://localhost:8000/api/v1/products/"
 O {"id":4,"name":"Glass","category":{"id":4,"name":"Crockery","status":1}}

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/products/"
 O {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Vessel",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 3,
            "name": "Stove",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 4,
            "name": "Glass",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        }
    ]
   }

12. Simply create the following dictionaries in api_urls.py to hold the http_method to python_method mapping.
 - ListCreateMapper = {
    'get':'list',
    'post':'create'
   }

 - RetrieveUpdateDestroyMapper = {
    'get':'retrieve',
    'delete':'destroy',
    'patch':'partial_update'
   }

13. What if we want to list all the Products under one Category? Let's nest our urls!
 - urlpatterns = [
    url(r'^categories/$', CategoryViewSet.as_view(ListCreateMapper), name='category-list'),
    url(r'^categories/(?P<pk>[0-9]+)/$', CategoryViewSet.as_view(RetrieveUpdateDestroyMapper), name='category-detail'),
    url(r'^categories/(?P<pk>[0-9]+)/products/$', ProductViewSet.as_view(ListCreateMapper), name='product-list'),
    url(r'^categories/(?P<pk>[0-9]+)/products/(?P<pk>[0-9]+)/$', ProductViewSet.as_view(RetrieveUpdateDestroyMapper), name='caproduct-detail'),
]
 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"
 X django.core.exceptions.ImproperlyConfigured: "^categories/(?P<pk>[0-9]+)/products/(?P<pk>[0-9]+)/$" is not a valid regular expression: redefinition of group name 'pk' as group 2; was group 1

 -  url(r'^categories/(?P<categories_pk>[0-9]+)/products/$', ProductViewSet.as_view(ListCreateMapper), name='product-list'),
    url(r'^categories/(?P<categories_pk>[0-9]+)/products/(?P<pk>[0-9]+)/$', ProductViewSet.as_view(RetrieveUpdateDestroyMapper), name='caproduct-detail')

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/"

 * curl -H "Content-Type:application/json" -X POST -d '{"name":"Chicken", "category_id":1}' "http://localhost:8000/api/v1/categories/1/products/"
 O {"id":6,"name":"Chicken","category":{"id":1,"name":"Meat","status":1}}

 * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/4/products/"
 X {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Vessel",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 3,
            "name": "Stove",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 4,
            "name": "Glass",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 5,
            "name": "Glass",
            "category": {
                "id": 1,
                "name": "Meat",
                "status": 1
            }
        },
        {
            "id": 6,
            "name": "Chicken",
            "category": {
                "id": 1,
                "name": "Meat",
                "status": 1
            }
        }
    ]
   }

14. Override get_queryset on the ProductViewSet.

 - def get_queryset(self):
        queryset = Product.objects.all()

        category_id = self.kwargs.get('categories_pk', None)
        product_id = self.kwargs.get('pk', None)

        if category_id:
            category = Category.objects.get(id=category_id)
            queryset = queryset.filter(category=category)

        if product_id:
            queryset = queryset.filter(id=product_id)

        return queryset

  * curl -H "Content-Type:application/json" -X GET "http://localhost:8000/api/v1/categories/4/products/"
  O {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Vessel",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 3,
            "name": "Stove",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        },
        {
            "id": 4,
            "name": "Glass",
            "category": {
                "id": 4,
                "name": "Crockery",
                "status": 1
            }
        }
    ]
   }
