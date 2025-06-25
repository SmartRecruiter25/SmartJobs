from django.forms import ModelForm
from django import forms
from .models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'featured_image',
            'description',
            'tags',
            'salary_range',
            'job_type',
            'location',
            'skills_required',
            'status',
        ]

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'skills_required': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})