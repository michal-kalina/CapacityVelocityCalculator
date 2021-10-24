from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Sprint

# Create your views here.
class SprintListView(ListView):
    template_name = 'sprint/sprint_list.html'
    context_object_name = 'output'
    model = Sprint
    paginate_by = 2

    def get_queryset(self):
        """Return the list of."""
        return Sprint.objects.order_by('-id')

class SprintDetailView(DetailView):
    model = Sprint
    context_object_name = 'output'

class SprintCreateView(CreateView): 
    model = Sprint
    context_object_name = 'output'
    fields = ['name']
    template_name_suffix = '_create_form'

class SprintUpdateView(UpdateView): 
    model = Sprint
    context_object_name = 'output'
    fields = ['name']
    template_name_suffix = '_update_form'

class SprintDeleteView(DeleteView): 
    model = Sprint
    context_object_name = 'output'
    success_url = reverse_lazy('sprint:sprints')