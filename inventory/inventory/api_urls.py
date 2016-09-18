from rest_framework import routers

from django.conf.urls import url

from products.views import UserViewSet

router = routers.SimpleRouter()

router.register(
    r'users',
    UserViewSet,
    base_name='user'
)

urlpatterns = router.urls
