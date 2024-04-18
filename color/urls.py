"""URLs for Color"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.api_over_view, name="api-overview"),
    path("color-list-all/", views.ColorListAllView.as_view(), name="color-list-all"),
    path("color-list/", views.ColorListView.as_view(), name="color-list"),
    path(
        "color-list-user/<str:user_id>",
        views.ColorListByUserIdView.as_view(),
        name="color-list-by-user",
    ),
    path(
        "color-detail/<str:pk>/", views.ColorDetailView.as_view(), name="color-detail"
    ),
    path("color-create/", views.ColorCreateView.as_view(), name="color-create"),
    path(
        "color-create-all/", views.ColorCreateAllView.as_view(), name="color-create-all"
    ),
    path(
        "color-update/<str:pk>/", views.ColorUpdateView.as_view(), name="color-update"
    ),
    path(
        "color-delete/<str:pk>/", views.ColorDeleteView.as_view(), name="color-delete"
    ),
]
