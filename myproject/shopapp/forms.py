from django import forms
from django.contrib.auth.models import Group

from shopapp.models import Product


# class ProductForm(forms.Form):
#     name = forms.CharField()
#     description = forms.CharField(max_length=100, widget=forms.Textarea)
#     price = forms.DecimalField(min_value=1, max_value=10000, decimal_places=2)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    images = MultipleFileField()


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',
