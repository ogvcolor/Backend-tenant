from django.urls import path

from . import views

urlpatterns = [
    path("", views.certification_over_view, name="certification-overview"),
    path(
        "get-reference/",
        views.ReferenceListAllView.as_view(),
        name="get-reference",
    ),
    path(
        "reference-user/<str:user_id>",
        views.ReferenceListByUserIdView.as_view(),
        name="reference-list-userr",
    ),
    path(
        "get-chart-proof/",
        views.ChartProofListAllView.as_view(),
        name="get-chart-proof",
    ),
    path(
        "chart-proof-user/<str:user_id>",
        views.ChartProofListByUserIdView.as_view(),
        name="chart-proof-user",
    ),
    path(
        "get-tolerance/",
        views.ToleranceListAllView.as_view(),
        name="get-tolerance",
    ),
    path(
        "create-dataset/",
        views.CreateCMYKDataSetView.as_view(),
        name="create-dataset",
    ),
    path(
        "cmyk-data-id/<str:data_id>/",
        views.CMYKDataListByDataIdView.as_view(),
        name="cmyk-data-id",
    ),
    path(
        "create-tolerance/",
        views.CreateToleranceSetView.as_view(),
        name="create-tolerance",
    ),
    path(
        "result-update/<str:pk>/",
        views.UpdateResultSetView.as_view(),
        name="result-update",
    ),
    path(
        "result-delete/<str:pk>/",
        views.DeleteResultView.as_view(),
        name="result-delete",
    ),
    path(
        "create-comparison-result/",
        views.CreateResultSetView.as_view(),
        name="create-comparison-result",
    ),
]
