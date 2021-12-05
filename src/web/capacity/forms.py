from django import forms
from django.forms.fields import IntegerField
from django.forms.formsets import ManagementForm, BaseFormSet, DEFAULT_MIN_NUM, DEFAULT_MAX_NUM, TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MIN_NUM_FORM_COUNT, MAX_NUM_FORM_COUNT
from django.forms.widgets import HiddenInput
from django.utils.functional import cached_property
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

# special field names
SAVE_RAWS = 'SAVE'
ADD_NEW_RAW = 'ADD'
ADD_NEW_RAW_COUNTER = 'ADD_COUNTER'
REMOVE_RAWS = 'DELETE'

# default value indicating that no new line was added to formset
DEFAULT_SAVE_RAWS = 0
DEFAULT_ADD_NEW_RAW = 0
DEFAULT_ADD_NEW_RAW_COUNTER = 0
DEFAULT_REMOVE_RAWS = 0

class SprintCapacityUpdatePersonManagementForm(ManagementForm):
    def __init__(self, *args, **kwargs):
        self.base_fields[SAVE_RAWS] = IntegerField(widget=HiddenInput)
        self.base_fields[ADD_NEW_RAW] = IntegerField(widget=HiddenInput)
        self.base_fields[ADD_NEW_RAW_COUNTER] = IntegerField(widget=HiddenInput)
        self.base_fields[REMOVE_RAWS] = IntegerField(widget=HiddenInput)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # When the management form is invalid, we don't know if new raw
        # was added.
        cleaned_data.setdefault(SAVE_RAWS, DEFAULT_SAVE_RAWS)
        cleaned_data.setdefault(ADD_NEW_RAW, DEFAULT_ADD_NEW_RAW)
        cleaned_data.setdefault(ADD_NEW_RAW_COUNTER, DEFAULT_ADD_NEW_RAW_COUNTER)
        cleaned_data.setdefault(REMOVE_RAWS, DEFAULT_REMOVE_RAWS)
        return cleaned_data

class SprintCapacityUpdatePersonFormset(BaseFormSet):
    def __init__(self, data) -> None:
        self.form = SprintCapacityUpdatePersonForm
        self.extra = {}
        self.can_order = False
        self.can_delete = True
        self.can_delete_extra = True
        self.min_num = DEFAULT_MIN_NUM
        self.max_num = DEFAULT_MAX_NUM
        self.absolute_max = self.max_num + DEFAULT_MAX_NUM
        self.validate_min = False
        self.validate_max = False,
        super().__init__(data=data)

    @cached_property
    def management_form(self):
        """Return the ManagementForm instance for this FormSet."""
        if self.is_bound:
            form = SprintCapacityUpdatePersonManagementForm(self.data, auto_id=self.auto_id, prefix=self.prefix)
            form.full_clean()
        else:
            form = SprintCapacityUpdatePersonManagementForm(auto_id=self.auto_id, prefix=self.prefix, initial={
                TOTAL_FORM_COUNT: self.total_form_count(),
                INITIAL_FORM_COUNT: self.initial_form_count(),
                MIN_NUM_FORM_COUNT: self.min_num,
                MAX_NUM_FORM_COUNT: self.max_num,
                SAVE_RAWS: DEFAULT_SAVE_RAWS,
                ADD_NEW_RAW: DEFAULT_ADD_NEW_RAW,
                ADD_NEW_RAW_COUNTER: DEFAULT_ADD_NEW_RAW_COUNTER,
                REMOVE_RAWS: DEFAULT_REMOVE_RAWS
            })
        return form