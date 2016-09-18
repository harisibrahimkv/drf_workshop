from rest_framework import routers

from django.conf.urls import patterns, url

router = routers.SimpleRouter()

router.register(
    r'users',
    UserViewSet,
    base_name='user'
)

urlpatterns = router.urls
