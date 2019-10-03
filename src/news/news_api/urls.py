from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')

urlpatterns = [
url(r'', include(router.urls)),
]
