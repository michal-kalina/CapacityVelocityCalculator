from django.forms import formsets
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
from .dtos import OutputDto, OutputItemDto
from .forms import SprintCapacityUpdatePersonFormset, ADD_NEW_RAW
from django.forms import formset_factory
from django.forms.formsets import DELETION_FIELD_NAME
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
        print(request.POST)
        formset = self.get_formset(request.POST)

        if formset.is_valid() and formset.management_form.cleaned_data.get(ADD_NEW_RAW) == 0:
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)    

    def get_formset(self, data: dict):
        """Return an instance of the form to be used in this view."""
        return SprintCapacityUpdatePersonFormset(data=data)

    def form_valid(self, formset):
        """If the form is valid, redirect to the supplied URL."""
        try:
            with transaction.atomic():
                # for form in formset.deleted_forms:
                #     capacity_to_delete: SprintCapacity = SprintCapacity.objects.get(id=form.cleaned_data.get('id'))
                #     capacity_to_delete.delete()
                
                for form in formset.forms:
                    # Change only forms that were not deleted an were changed
                    if form.has_changed() and not form.cleaned_data.get(DELETION_FIELD_NAME) and not form.cleaned_data.get('ADD'):
                        # Update person in sprint capacity only if user selected it from list
                        if form.cleaned_data.get('persons').id > 0:
                            person: Person = Person.objects.get(id=form.cleaned_data.get('persons').id)
                            capacity: SprintCapacity = SprintCapacity.objects.get(id=form.cleaned_data.get('id'))
                            capacity.person = person
                            capacity.save()

                    # Add new sprint capacity
                    if form.has_changed() and form.cleaned_data.get(ADD_NEW_RAW):
                        pass

        except IntegrityError as ex: #If the transaction failed
            print(ex)
            # messages.error(request, 'There was an error saving your profile.')
            return self.render_to_response(self.get_context_data(formset=formset))
        except SprintCapacity.DoesNotExist as ex:
            print(ex)
        except Person.DoesNotExist as ex:
            print(ex)

        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, formset):
        """If the form is invalid, render the invalid form."""
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(**{'formset': formset, 'object': self.object}))

    def get_context_data(self, **kwargs):
        def get_initial_formset(output: OutputDto) -> SprintCapacityUpdatePersonFormset:
            data = {
                'form-TOTAL_FORMS': f'{output.size}',
                'form-INITIAL_FORMS': f'{output.size}',
                'form-ADD': '0',
                'form-ADD_COUNTER': '0',
                'form-DELETE': '0'
            }
            # initialize formset forms with data
            for i in range(0, output.size):
                data.update({
                    f'form-{i}-id': output.items[i].id,
                    f'form-{i}-sprint_id': output.sprint_id,
                    f'form-{i}-persons': output.items[i].person_id,
                })
            return self.get_formset(data)

        def add_item_to_formset(formsetData: dict, output: OutputDto) -> SprintCapacityUpdatePersonFormset:
            new_row_counter = int(formsetData['form-ADD_COUNTER'])
            size = output.size
            full_size = size + new_row_counter
            
            # Set variables
            formsetData.update({
                'form-ADD': '0',
                'form-ADD_COUNTER': f'{new_row_counter}',
                'form-TOTAL_FORMS': f'{full_size}'
            })

            for index in range(size, full_size):
                # Increasing elements by one dummy item
                output.append_empty_item()
                # if the key is present, skip it
                if f'form-{index}-id' not in formsetData:
                    formsetData.update({
                        # Adding new form data
                        f'form-{index}-id': '0',
                        f'form-{index}-sprint_id': output.sprint_id,
                        f'form-{index}-persons': '0'
                    })

            return (self.get_formset(formsetData), output)

        def remove_item_from_formset(formsetData: dict, output: OutputDto) -> SprintCapacityUpdatePersonFormset:
            row_counter = int(formsetData['form-ADD_COUNTER'])
            size = output.size
            full_size = size + row_counter

            for index in range(0, full_size):
                if f'form-{index}-DELETE' in formsetData and formsetData[f'form-{index}-DELETE'] == 'on':
                    if formsetData[f'form-{index}-id'] == '0':
                        # Set variables only for elements artificially added
                        row_counter = row_counter - 1
                        formsetData.update({
                            'form-ADD_COUNTER': f'{row_counter}',
                        })
                    formsetData[f'form-{index}-DELETE'] = ''
                    del formsetData[f'form-{index}-id']
                    del formsetData[f'form-{index}-sprint_id']
                    del formsetData[f'form-{index}-persons']
                    output.remove_at(index)
                else:
                    if index >= output.size and output.size > row_counter:
                        # We need to add empty item after moving beyond output elements
                        output.append_empty_item()

            # Set variables
            formsetData.update({
                'form-DELETE': '0',
                'form-TOTAL_FORMS': f'{output.size + row_counter}'
            })

            return (self.get_formset(formsetData), output)

        if('formset' in kwargs):
            formsetDict = kwargs['formset'].data.dict()
            # Add item
            if 'form-ADD' in formsetDict and formsetDict['form-ADD'] == '1':
                formset, self.object = add_item_to_formset(formsetDict, kwargs['object'])
            elif 'form-DELETE' in formsetDict and formsetDict['form-DELETE'] == '1':
                formset, self.object = remove_item_from_formset(formsetDict, kwargs['object'])
            else:
                formset = get_initial_formset(self.object)
        else:
            formset = get_initial_formset(self.object)

        print(self.object)
        print(formset.data)
        context = super(SprintCapacityUpdateView, self).get_context_data(**kwargs)
        context['object'] = self.object
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
