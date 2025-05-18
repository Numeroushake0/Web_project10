from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Quote

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'born_date', 'born_location', 'description']
        widgets = {
            'born_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']
        widgets = {
            'quote': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.CheckboxSelectMultiple(),
        }
