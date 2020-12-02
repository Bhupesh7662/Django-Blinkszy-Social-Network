from django.urls import path
from . import views
from .views import Change_Password

urlpatterns = [
    path('', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path("change_password", views.Change_Password.as_view(), name='change_password')
]
