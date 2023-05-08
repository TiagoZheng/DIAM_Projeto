from django.urls import include, path
from . import views


app_name = 'home'
urlpatterns = [
    # ex: home/
    path('', views.index, name='index'),

    # ex: home/login/
    path('login/', views.login_view, name='login'),

    path('registration/', views.registration, name='registration'),
]
