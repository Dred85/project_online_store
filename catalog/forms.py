from datetime import datetime

from django import forms

from .mixins import StyledFormMixin
from .models import Contact, Product, Version


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'address', 'message']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        PROHIBITED_WORDS = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
        ]
        cleaned_data = self.cleaned_data['name']
        for word in PROHIBITED_WORDS:
            if word in cleaned_data.lower():
                raise forms.ValidationError("Имя не должно содержать запрещенные слова:'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.created_at = datetime.now()
        instance.updated_at = datetime.now()
        if commit:
            instance.save()
        return instance


class ProductVersionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_number', 'version_name')
