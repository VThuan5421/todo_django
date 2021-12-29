from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("", views.index, name = "index"),
    path("login/", views.user_login, name = "user_login"),
    path("registration/", views.user_registration, name = "user_registration"),
    path("logout/", views.Logout, name = "Logout"),
    path("delete_task/<int:myid>/", views.delete_task, name = "delete_task"),
    path("edit_task/<int:myid>/", views.edit_task, name = "edit_task"),


]