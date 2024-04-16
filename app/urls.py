from django.contrib import admin
from django.urls import path, include
from app.views import ClientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r"client", ClientViewSet, basename="clients")

urlpatterns = [
       path('admin/', admin.site.urls),
    path("", include(router.urls)),
]
