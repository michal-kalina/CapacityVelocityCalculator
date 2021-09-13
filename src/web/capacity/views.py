from django.shortcuts import render
from django.http import HttpResponse

from .models import SprintCapacity, Sprint

# Create your views here.
def index(request):
    current_sprint = Sprint.objects.last()
    current_sprint_capacity = SprintCapacity.objects.filter(sprint_id=current_sprint.id).order_by("id")

    return HttpResponse("Hello this is capacity calculator index page!")