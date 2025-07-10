from django import forms
from .models import Event, Category

class StyledFormMixin:
    """ Mixing to apply style to form field"""
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })

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
        fields = ['name', 'description', 'date', 'time', 'location', 'category','event_image']


# class ParticipantForm(forms.ModelForm):
#     name = forms.CharField(label='Participant Name')
#     email = forms.EmailField(label='Email Address')
#     events = forms.ModelMultipleChoiceField(
#         label='Select Events',
#         queryset=Event.objects.all(),
#         widget=forms.CheckboxSelectMultiple()
#     )

#     class Meta:
#         model = Participant
#         fields = ['name', 'email', 'events']
