"""URLs for Device Configuration"""

from django.urls import path

from . import views

urlpatterns = [
    path(
        "get-measure-all-response/",
        views.GetAllMeasureResponse.as_view(),
        name="get-measure-all-response",
    ),
    path(
        "get-measure-response/<str:pk>/",
        views.GetMeasureResponseById.as_view(),
        name="create-measure-response/",
    ),
    path(
        "create-measure-request/",
        views.CreateMeasureRequest.as_view(),
        name="create-measure-request/",
    ),
    path(
        "delete-measure-request/<str:pk>/",
        views.DeleteMeasureRequest.as_view(),
        name="delete-measure-request/",
    ),
]
