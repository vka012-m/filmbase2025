from django import forms
from dal import autocomplete
from .models import Country, Genre, Film, Person, Award, Nomination, Result


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['name', 'origin_name', 'slogan', 'length', 'year',
                  'trailer_url', 'cover', 'description', 'country', 'genres',
                  "director", 'people']
        widgets = {
            'people': autocomplete.ModelSelect2Multiple(
                url='films:person_autocomplete'),
            'director': autocomplete.ModelSelect2(
                url='films:person_autocomplete'),
            'country': autocomplete.ModelSelect2(
                url='films:country_autocomplete'),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'origin_name', 'birthday', 'photo']
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'},
                                        format="%Y-%m-%d")
        }

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['name', 'year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year < 1900 or year > 2026:
            raise forms.ValidationError("Год должен быть от 1900 до 2026.")
        return year

class NominationForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = ['name', 'award']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'award': forms.Select(attrs={'class': 'form-control'}),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['nomination', 'person', 'film', 'is_won']
        widgets = {
            'nomination': forms.Select(attrs={'class': 'form-control'}),
            'person': forms.Select(attrs={'class': 'form-control'}),
            'film': forms.Select(attrs={'class': 'form-control'}),
            'is_won': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }