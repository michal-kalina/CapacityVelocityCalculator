from django.urls import path

from . import views

app_name = "person"
urlpatterns = [
    path('', views.PersonListView.as_view(), name='persons'),
	path('<int:pk>', views.PersonDetailView.as_view(), name='detail'),
	path('create', views.PersonCreateView.as_view(), name='create'),
	path('update/<int:pk>', views.PersonUpdateView.as_view(), name='update'),
	path('delete/<int:pk>', views.PersonDeleteView.as_view(), name='delete'),
]