from django.urls import path

from . import views

app_name = "capacity"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:sprint_id>", views.details, name="details"),
    path("update/", views.update, name="update")
]