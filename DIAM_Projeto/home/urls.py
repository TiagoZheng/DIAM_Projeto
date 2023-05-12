from django.urls import include, path
from . import views

app_name = 'home'

urlpatterns = [
    # ex: home/
    path('', views.index, name='index'),

    # ex: home/1
    path('<int:post_id>/', views.details, name='details'),

    # ex: home/login_view/
    path('login/', views.login_view, name='login'),

    # ex: home/registration
    path('register/', views.register, name='register'),

    # ex: home/new_post/
    path('new_post/', views.new_post, name='new_post'),

    # ex: home/logout
    path('logout/', views.user_logout, name='logout'),

    # ex: home/profile
    path('profile/', views.profile, name='profile'),

    path('<int:post_id>/like/', views.like, name='like'),

    path('<int:post_id>/write_comment', views.write_comment, name='write_comment'),

    path('profile/delete/<int:post_id>/', views.delete_post, name='delete_post'),

]
