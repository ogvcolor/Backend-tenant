from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.views import ClientViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"client", ClientViewSet, basename="clients")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
