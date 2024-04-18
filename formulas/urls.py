from django.urls import path

from . import views

urlpatterns = [
    path("get-lab/", views.GetLabView.as_view(), name="get-LAB"),
    path("get-all-lab/", views.GetLabAllView.as_view(), name="get-all-LAB"),
    path("get-lchab/", views.GetLchabView.as_view(), name="get-LCHab"),
    path("get-RGB/", views.GetRgbView.as_view(), name="get-RGB"),
    path("get-all-RGB/", views.GetRgbAllView.as_view(), name="get-all-RGB"),
    path("get-min-deltae/", views.GetMinDeltaEView.as_view(), name="get-min-deltae"),
    path("get-max-deltae/", views.GetMaxDeltaEView.as_view(), name="get-max-deltae"),
    path(
        "get-deltaeh-from-lab/",
        views.GetDeltaEHfromLabView.as_view(),
        name="get-deltaeh-from-lab",
    ),
]
