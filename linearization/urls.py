from django.urls import path
from . import views


urlpatterns = [
    path('linearization/', views.LinearizationView.as_view(), name="lienarization"),
    path('get-interpolation/', views.InterpolationView.as_view(), name="interpolation"),
    path('get-color-sets/<str:target_set>/', views.ColorSetListView.as_view(), name="get-color-sets"),
    path('create-color-set/', views.ColorSetCreateView.as_view(), name="create-color-set"),
    path('create-all-color-set/', views.ColorSetCreateAllView.as_view(), name="create-all-color-set"),
    path('update-color-set/<str:pk>/', views.ColorSetUpdateView.as_view(), name="update-color-set"),
    path('delete-color-set/<str:pk>/', views.ColorSetDeleteView.as_view(), name="delete-color-set"),
    path('get-default-target-sets/', views.TargetSetListDefaultView.as_view(), name="get-target-set"),
    path('get-target-sets/', views.TargetSetListAllView.as_view(), name="get-default-target-set"),
    path('get-target-sets-user-only/<str:user_id>/', views.TargetSetListOnlyByUserIdView.as_view(), name="get-target-sets-user-only"),
    path('get-target-sets-user/<str:user_id>/', views.TargetSetListByUserIdView.as_view(), name="get-target-set"),
    path('create-target-set/', views.TargetSetCreateView.as_view(), name="create-target-set"),
    path('update-target-set/<str:pk>/', views.TargetSetUpdateView.as_view(), name="update-target-set"),
    path('delete-target-set/<str:pk>/', views.TargetSetDeleteView.as_view(), name="delete-target-set"),
    path('get-projects/', views.CalibrationListAllView.as_view(), name="get-all-projects"),
    path('get-projects-user/<str:user_id>/', views.CalibrationListByUserIdView.as_view(), name="get-projects-user"),
    path('project-create/', views.CalibrationCreateView.as_view(), name='project-create'),
    path('project-update/<str:pk>/', views.CalibrationUpdateView.as_view(), name='project-update'),
    path('project-delete/<str:pk>/', views.CalibrationDeleteView.as_view(), name='project-update'),
    path('get-measures/', views.MeasuredListAllView.as_view(), name="get-all-measured"),
    path('create-measures/', views.MeasuredCreateView.as_view(), name='create-measures'),
    path('measures-update/<str:pk>/', views.MeasuredUpdateView.as_view(), name='measures-update'),
]