from django.urls import include, path
from rest_framework import routers

# Projects imports
from data_processing import views

routes = routers.DefaultRouter()

routes.register("data-processing", views.AnalyseData, basename="Data Processing")

urlpatterns = [path("", include(routes.urls))]
