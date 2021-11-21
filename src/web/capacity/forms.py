from django import forms
from .models import Person 

class SprintCapacityUpdatePersonForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput()) 
    sprint_id = forms.IntegerField(widget=forms.HiddenInput())
    persons = forms.ModelChoiceField(widget = forms.Select(), queryset=Person.objects.all(), required = True, label="")

    def as_table(self):
        "Return this form rendered as HTML."
        return self._html_output(
            normal_row='<div>%(errors)s%(field)s%(help_text)s</div>',
            error_row='<div>%s</div>',
            row_ender='</div>',
            help_text_html='<br><span class="helptext">%s</span>',
            errors_on_separate_row=False,
        )