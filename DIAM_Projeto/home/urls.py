from django.urls import include, path
from . import views
from django.views.generic import TemplateView

app_name = 'home'

urlpatterns = [
    # ex: home/
    path('', views.index, name='index'),

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

    path('not_logged_error/', TemplateView.as_view(template_name='home/not_logged_error.html'),name='not_logged_error'),

    path('my_groups', views.my_groups, name='my_groups'),

    path('my_groups/create_group', views.create_group, name='create_group'),

    path('my_groups/group_detail/<int:group_id>/', views.group_detail, name='group_detail'),

    path('my_groups/group_detail/delete_group/<int:group_id>/', views.delete_group, name='delete_group'),

    path('my_groups/group_detail/<int:group_id>/add_group_member/', views.add_group_member, name='add_group_member'),

    path('my_groups/group_detail/<int:group_id>/delete_member/', views.delete_member, name='delete_member'),

    path('my_groups/group_detail/<int:group_id>/new_group_post/', views.new_group_post, name='new_group_post'),

]
