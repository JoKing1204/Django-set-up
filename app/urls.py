from django.urls import path
from .views import basic_home, admin_home, create_item, update_item, delete_item, logout_user, login_user, register_user,read_items
urlpatterns = [
    path('basic_user_home/', basic_home, name='basic_user_home'),
    path('admin_home/', admin_home, name="admin_home"),
    path('create/', create_item, name='create_item'),
    path('update/<int:item_id>/', update_item, name="update_item"),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path("", register_user, name="register"),
    path("login/",login_user, name="login"),
    path('logout/', logout_user, name='logout'),
    path('read_items/', read_items, name='read_items')

]
