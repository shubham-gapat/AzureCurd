from django.urls import path
from .views import AddUser, UpdateUser, UpdateUserPassword, DeleteUser

urlpatterns = [
    path("add_user", AddUser.as_view(), name="add_user"),
    path("update_user", UpdateUser.as_view(), name="update_user"),
    path("delete_user", DeleteUser.as_view(), name="delete_user"),
    path("user_password_update", UpdateUserPassword.as_view(), name="user_password_update"),
]
