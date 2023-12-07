from django.urls import path
from . import views
urlpatterns = [
    path('signup',views.User_signup, name = "signup"),
    path('login',views.User_login, name = "login"),
]
