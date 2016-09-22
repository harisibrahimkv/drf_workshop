from rest_framework import routers

from django.conf.urls import url

from products.views import (
    UserViewSet,
    CategoryViewSet,
    ProductViewSet,
    StatViewSet
)

router = routers.SimpleRouter()

router.register(
    r'users',
    UserViewSet,
    base_name='user'
)

# router.register(
#     r'categories',
#     CategoryViewSet,
#     base_name='category'
# )

router.register(
    r'stats',
    StatViewSet,
    base_name='stat'
)

router.register(
    r'products',
    ProductViewSet,
    base_name='product'
)

urlpatterns = [
    url(r'^categories/$', CategoryViewSet.as_view({'get':'list', 'post':'create'}), name='category-list'),
    url(r'^categories/(?P<pk>[0-9]+)/$', CategoryViewSet.as_view({'get':'retrieve', 'delete':'destroy', 'patch':'partial_update'}), name='category-detail'),
]

urlpatterns += router.urls
