from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.db.models import QuerySet
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic import View
from django.urls import reverse_lazy
from .models import Person, SprintCapacity, Sprint, SprintCapacityPresenceItem
from .dtos import OutputDto
from .forms import SprintCapacityUpdatePersonForm
from django.forms import formset_factory
from django.db import IntegrityError, transaction



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

class SprintCapacityUpdateView(DetailView): 
    model = Sprint
    template_name = 'capacity/sprintcapacity_update_form.html'
    context_object_name = 'output'
    pk_url_kwarg = 'sprint_id'
    success_url = reverse_lazy('capacity:current')

    def get_object(self):
        output = OutputDto(self.kwargs['sprint_id'])
        return output

    def get(self, request, *args, **kwargs):
        super(SprintCapacityUpdateView, self).get(request, *args, **kwargs)
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(request.POST)

        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)    

    def get_formset(self, data: dict):
        """Return an instance of the form to be used in this view."""
        SprintCapacityUpdatePersonFormset = formset_factory(SprintCapacityUpdatePersonForm)
        return SprintCapacityUpdatePersonFormset(data=data)

    def form_valid(self, formset):
        """If the form is valid, redirect to the supplied URL."""

        try:
            with transaction.atomic():
                for form in formset.forms:
                    # TODO: Handle 0 id for person
                    person: Person = Person.objects.get(id=form.cleaned_data.get('persons').id)
                    capacity: SprintCapacity = SprintCapacity.objects.get(id=form.cleaned_data.get('id'))
                    capacity.person = person
                    capacity.save()
        except IntegrityError: #If the transaction failed
            # messages.error(request, 'There was an error saving your profile.')
            return self.render_to_response(self.get_context_data(formset=formset))
        except SprintCapacity.DoesNotExist as ex:
            print(ex)
        except Person.DoesNotExist as ex:
            print(ex)

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, formset):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_context_data(self, **kwargs):
        object = self.get_object()
        # initialize formset data
        data = {
            'form-TOTAL_FORMS': f'{len(object.items)}',
            'form-INITIAL_FORMS': f'{len(object.items)}'
        }
        # initialize formset forms with data
        for i in range(0, len(object.items)):
            data.update({
                f'form-{i}-id': object.items[i].id,
                f'form-{i}-sprint_id': object.sprint_id,
                f'form-{i}-persons': object.items[i].person_id,
            })
        formset = self.get_formset(data)
        context = super(SprintCapacityUpdateView, self).get_context_data(**kwargs)
        context['object'] = object
        context['formset'] = formset
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
