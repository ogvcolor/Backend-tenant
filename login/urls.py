from django.urls import path
from . import views
from knox.views import LogoutView, LogoutAllView

urlpatterns = [
    #path('user/', views.get_user),
    path('register/', views.CreateUserAPI.as_view()),
    path('update-user/<str:pk>', views.UpdateUserAPI.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
    #path('user_all/', views.get_all_users),
    #path('login/', views.accounts)
]

""" urlpatterns = [
    path('register/', views.UserRegister.as_view(), name="register"),
    path('login/', views.UserLogin.as_view(), name="login"),
    path('logout/', views.UserLogout.as_view(), name="logout"),
    path('user/', views.UserView.as_view(), name="user"),
] """