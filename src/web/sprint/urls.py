from django.urls import path

from . import views

app_name = "sprint"
urlpatterns = [
    path('', views.SprintListView.as_view(), name='sprints'),
	path('<int:pk>', views.SprintDetailView.as_view(), name='detail'),
	path('create', views.SprintCreateView.as_view(), name='create'),
	path('update/<int:pk>', views.SprintUpdateView.as_view(), name='update'),
	path('delete/<int:pk>', views.SprintDeleteView.as_view(), name='delete'),
]