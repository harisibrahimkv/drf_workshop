from rest_framework import routers

from django.conf.urls import url

from products.views import UserViewSet, CategoryViewSet

router = routers.SimpleRouter()

router.register(
    r'users',
    UserViewSet,
    base_name='user'
)

router.register(
    r'categories',
    CategoryViewSet,
    base_name='category'
)

urlpatterns = router.urls
