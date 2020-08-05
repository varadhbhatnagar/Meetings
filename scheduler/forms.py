from django import forms
import datetime
from .util import get_slots
from .models import Meeting

DURATION_CHOICES =( 
    ("15", "15 Minutes"), 
    ("30", "30 Minutes"), 
    ("45", "45 Minutes"), 
    ("60", "1 Hour"), 
    ("90", "1.5 Hour"),
    ("120", "2 Hours"), 
    ("150", "2.5 Hours"), 
    ("180", "3 Hours"),
    ("210", "3.5 Hours"),  
    ("240", "4 Hours"),    
)


class OrganiserForm(forms.Form):
    contact = forms.CharField(required=True)
    duration = forms.ChoiceField(choices =DURATION_CHOICES)
    date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(), required=True)
    title = forms.CharField(required=True)

class ParticipantForm(forms.Form):
    def __init__(self, meeting_hash, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields['slot'].choices = get_slots(int(Meeting.objects.get(meeting_hash = meeting_hash).duration))
        self.fields['meeting_hash'].queryset =meeting_hash

    contact = forms.CharField(required=True)
    slot = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=())
    meeting_hash = forms.CharField()