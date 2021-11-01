from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404
from django.db.models import QuerySet
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Person, SprintCapacity, Sprint, SprintCapacityPresenceItem
from .dtos import OutputDto, OutputItemDto, OutputItemPresenceDto, OutputStringDto



class SprintCapacityDetailView(DetailView):
    model = Sprint
    template_name = 'capacity/sprintcapacity_detail.html'
    context_object_name = 'output'
    pk_url_kwarg = 'sprint_id'
    
    def get_context_data(self, **kwargs):
        context = super(SprintCapacityDetailView, self).get_context_data(**kwargs)
        sprint_id = self.kwargs['sprint_id']
        output = OutputDto(sprint_id)
        context['output'] = output
        return context

class SprintCapacityCreateView(CreateView): 
    model = SprintCapacity
    context_object_name = 'output'
    fields = ['name', 'surname']
    template_name_suffix = '_create_form'

class SprintCapacityUpdateView(UpdateView): 
    model = Sprint
    template_name = 'capacity/sprintcapacity_update_form.html'
    context_object_name = 'output'
    pk_url_kwarg = 'sprint_id'
    success_url = reverse_lazy('capacity:current')

    def get_object(self):
        try:
            obj: QuerySet[SprintCapacity] = SprintCapacity.objects.filter(sprint__id=self.kwargs['sprint_id'])
        except SprintCapacity.DoesNotExist:
            obj: QuerySet[SprintCapacity] = []
        return obj
    
    def get_persones(self):
        try:
            obj: QuerySet[Person] = Person.objects.all()
        except Person.DoesNotExist:
            obj: QuerySet[Person] = []
        return obj

    def get_context_data(self, **kwargs):
        context = super(SprintCapacityUpdateView, self).get_context_data(**kwargs)
        sprint_id = self.kwargs['sprint_id']
        objects = self.get_object()
        items = []
        for item in objects:
            kwargs['object'][items] = self.get_object()
            kwargs['object'] = self.get_persones().exclude()

        kwargs['output']['items'] = items
        return context

class SprintCapacityDeleteView(DeleteView): 
    model = SprintCapacity
    context_object_name = 'output'
    success_url = reverse_lazy('capacity:current')

def index(request):
    last_five_sprints: QuerySet[Sprint] = Sprint.objects.order_by("-id")[:5]
    output: list[OutputStringDto] = list[OutputStringDto]()
    for sprint in last_five_sprints:
        output.append(OutputStringDto(sprint.id, sprint.name))
    context = {
        'output': output,
    }
    return render(request, 'capacity/index.html', context)

def current(request):
    current_sprint: QuerySet[Sprint] = Sprint.objects.latest('-id')
    print(current_sprint)
    return redirect(reverse('capacity:details', kwargs={'sprint_id': current_sprint.id})) # We redirect to the same view

def update(request):
    if request.method == 'POST':
        id = request.POST['id']
        presence = request.POST['presence']
        date = request.POST['date']
        try:
            
            presenceItem: QuerySet[SprintCapacityPresenceItem] = get_object_or_404(SprintCapacityPresenceItem, id=id)
            if(presence in SprintCapacityPresenceItem.PRESENCE_CHOICES[0]): # Is in Yes tuple
                presenceItem.presence, _ = SprintCapacityPresenceItem.PRESENCE_CHOICES[1] # N
            else: # Is in no tuple
                presenceItem.presence, _ = SprintCapacityPresenceItem.PRESENCE_CHOICES[0] # Y
            presenceItem.save()
            sprint_id = presenceItem.sprint_capacity.sprint.id
            return redirect(reverse('capacity:details', kwargs={'sprint_id': sprint_id})) # We redirect to the same view
        except SprintCapacityPresenceItem.DoesNotExist as e:
            raise Http404(f"No SprintCapacityPresenceItem matches the given id: {id}.")
