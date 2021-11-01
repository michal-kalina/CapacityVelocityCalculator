from django.urls import path, re_path

from . import views

app_name = "capacity"
urlpatterns = [
    path("<int:sprint_id>", views.SprintCapacityDetailView.as_view(), name="details"),
	path('update/<int:sprint_id>', views.SprintCapacityUpdateView.as_view(), name='update'),
    path("current/", views.current, name="current"),
    path("update/", views.update, name="update")
]