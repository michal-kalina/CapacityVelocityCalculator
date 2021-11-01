from django import forms
from .models import Person 

class SprintCapacityUpdatePersonForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput()) 
    sprint_id = forms.IntegerField(widget=forms.HiddenInput())
    persons = forms.ModelChoiceField(widget = forms.Select(), queryset=Person.objects.all(), required = True)

    def __init__(self, id, sprint_id, choices_initial, choices):
        super(SprintCapacityUpdatePersonForm, self).__init__()
        self.fields['id'].initial = id
        self.fields['sprint_id'].initial = sprint_id
        self.fields['persons'].initial = choices_initial
        self.fields['persons'].choices = choices