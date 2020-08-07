from django import forms
import datetime
from .util import get_slots
from .models import Meeting, Participant

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

AVAILABILITY_CHOICES =( 
    ("1", "I am free in the following slots"), 
    ("2", "I am NOT free in the following slots"),  
)


class OrganiserForm(forms.Form):
    organiser_contact_number = forms.CharField(required=True)
    meeting_duration = forms.ChoiceField(choices =DURATION_CHOICES, required=True)
    meeting_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(), required=True)
    meeting_agenda = forms.CharField(required=True)


class ParticipantForm(forms.Form):
    def __init__(self, meeting_hash, *args, **kwargs):
        
        super(ParticipantForm, self).__init__(*args, **kwargs)
        self.fields['slot'].choices = get_slots(int(Meeting.objects.get(meeting_hash = meeting_hash).duration))
        self.fields['meeting_hash'].initial = meeting_hash
        self.fields['organiser_contact_number'].initial = Meeting.objects.get(meeting_hash = meeting_hash).organiser.contact
        self.fields['meeting_agenda'].initial = Meeting.objects.get(meeting_hash = meeting_hash).title
        self.fields['meeting_date'].initial = Meeting.objects.get(meeting_hash = meeting_hash).date

    organiser_contact_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    meeting_agenda = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    meeting_date = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    participant_contact_number = forms.CharField(required=True)
    availability = forms.ChoiceField(choices=AVAILABILITY_CHOICES)
    slot = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=(), required=False)
    meeting_hash = forms.CharField(widget=forms.HiddenInput())


class ResponseForm(forms.Form):

    meeting_agenda = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    organiser_contact_number = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    meeting_hash = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    best_slots = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    response_count = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'rea, donly'}))