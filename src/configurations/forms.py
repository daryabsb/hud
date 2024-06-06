from django import forms
from src.configurations.models import ApplicationProperty


class ConfigurationForm(forms.ModelForm):

    class Meta:
        model = ApplicationProperty
        fields = (
            'name',
            'value',
            'title',
            'description',
            'input_type',
            'editable',
            'params',
            'section',
        )


class ApplicationPropertyForm(forms.ModelForm):

    class Meta:
        model = ApplicationProperty
        fields = (
            'value',
        )
