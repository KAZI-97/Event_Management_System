from django import forms
from .models import Event, Category, Participant

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Category_Name')
    description = forms.CharField(label='Description')

    class Meta:
        model = Category
        fields = ['name', 'description']


class EventForm(forms.ModelForm):
    name = forms.CharField(label='Event Name')
    description = forms.CharField(label='Description')
    date = forms.DateField(label='Event Date', widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(label='Event Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    location = forms.CharField(label='Location')
    category = forms.ModelChoiceField(label='Event Category', queryset=Category.objects.all())

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']


class ParticipantForm(forms.ModelForm):
    name = forms.CharField(label='Participant Name')
    email = forms.EmailField(label='Email Address')
    events = forms.ModelMultipleChoiceField(
        label='Select Events',
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
