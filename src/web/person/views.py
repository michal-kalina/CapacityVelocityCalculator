from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Person
# Create your views here.
class PersonListView(ListView):
    template_name = 'person/person_list.html'
    context_object_name = 'output'
    model = Person
    paginate_by = 2

    def get_queryset(self):
        """Return the list of."""
        return Person.objects.order_by('-id')

class PersonDetailView(DetailView):
    model = Person
    context_object_name = 'output'

class PersonCreateView(CreateView): 
    model = Person
    context_object_name = 'output'
    fields = ['name', 'surname']
    template_name_suffix = '_create_form'

class PersonUpdateView(UpdateView): 
    model = Person
    context_object_name = 'output'
    fields = ['name', 'surname']
    template_name_suffix = '_update_form'

class PersonDeleteView(DeleteView): 
    model = Person
    context_object_name = 'output'
    success_url = reverse_lazy('person:persons')