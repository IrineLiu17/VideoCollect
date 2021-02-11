from .models import Video, Hall
from django import forms
from django.db import models
from django_mysql.forms import SimpleListField
from django.forms import modelformset_factory

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields=['url','title']
        labels={'url':'YouTube URL'}
        widgets = {'Id': forms.HiddenInput()}

VideoFormSet = modelformset_factory(
    Video, form = VideoForm, extra=1
)

class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='Search for Videos:')

class CreateForm(forms.ModelForm):
    # title = forms.CharField()
    # tags = SimpleListField(models.CharField(max_length=20),widget=forms.TextInput(attrs={'data-role': 'tagsinput','id':'taginput'}))
    class Meta:
        model = Hall
        fields=['title','tags']
        widgets = {
            'tags': forms.TextInput(attrs={'data-role': 'tagsinput','id':'taginput'}),
        }