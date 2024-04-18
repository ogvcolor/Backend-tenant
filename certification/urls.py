from django.urls import path

from . import views

urlpatterns = [
    path("", views.standard_over_view, name="standard-overview"),
    path(
        "get-cmyk-dataset/",
        views.CMYKDataSetListAllView.as_view(),
        name="get-cmyk-dataset",
    ),
    path(
        "cmyk-dataset-user/<str:user_id>",
        views.CMYKDataSetListByUserIdView.as_view(),
        name="cmyk-dataset-list-userr",
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
        "create-cmyk-dataset/",
        views.CreateCMYKDataSetView.as_view(),
        name="create-cmyk-dataset",
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
        views.UpdateComparisonResultSetView.as_view(),
        name="result-update",
    ),
    path(
        "result-delete/<str:pk>/",
        views.DeleteComparisonResultView.as_view(),
        name="result-delete",
    ),
    path(
        "create-comparison-result/",
        views.CreateComparisonResultsSetView.as_view(),
        name="create-comparison-result",
    ),
]
