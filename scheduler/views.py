from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import OrganiserForm, ParticipantForm
from .models import Meeting, Participant, MeetingParticipant, MeetingParticipantSlot
from .util import get_random_alphanumeric_string, update_best_slots, NUMBER_OF_MINUTES_IN_A_DAY


def organiser_view(request):

    if request.method == 'GET':
        form = OrganiserForm()
        return render(request, 'organiser_page.html', {'form': form})

    else: #POST
        form = OrganiserForm(request.POST, request.FILES)
        if form.is_valid():

            global SLOT_CHOICES
            organiser = Participant()
            organiser.contact = form.cleaned_data['contact']
            organiser.save()

            meeting = Meeting()
            meeting.meeting_hash = get_random_alphanumeric_string()
            meeting.organiser = organiser
            meeting.duration = form.cleaned_data['duration']
            meeting.date = form.cleaned_data['date']
            meeting.title = form.cleaned_data['title']
            meeting.save()

            meeting_participant = MeetingParticipant()
            meeting_participant.meeting = meeting
            meeting_participant.participant = organiser
            meeting_participant.save()

            meeting_participant_slot = MeetingParticipantSlot()
            meeting_participant_slot.meeting_participant = meeting_participant
            # meeting_participant_slot.slot = form.cleaned_data['slot']
            meeting_participant_slot.save()

            message = 'New Meeting Created. Invite participants by sending link : /meeting/{}'.format(meeting.meeting_hash)

        else:
            print("Form Invalid")
            print("Form Errors : ", str(form.errors))

            message = 'Form has errors. Please try again!'

    template = loader.get_template("form_response.html")
    context = {'message': message}
    return HttpResponse(template.render(context, request))


def participant_view(request, meeting_hash):

    if request.method == 'GET':
        form = ParticipantForm(meeting_hash)
        return render(request, 'participant_page.html', {'form': form})

    else: #POST
        form = ParticipantForm(request.POST, request.FILES)

        if form.is_valid():
            participant = Participant()
            participant.contact = form.cleaned_data['contact']
            participant.save()

            meeting_participant = MeetingParticipant()
            meeting_participant.participant = participant
            meeting_participant.meeting = Meeting.objects.get(meeting_hash = form.cleaned_data['meeting_hash'])
            meeting_participant.save()

            message = 'Thanks for Answering'

        else:
            print("Form Invalid")
            print("Form Errors : ", str(form.errors))

            message = 'Form has errors. Please try again!'

    template = loader.get_template("form_response.html")
    context = {'message': message}
    return HttpResponse(template.render(context, request))


def response_view(request, meeting_hash):
    
    meeting = Meeting.objects.get(meeting_hash = meeting_hash)
    meeting_participants = MeetingParticipant.objects.filter(meeting=meeting)

    best_slots = [0] * (NUMBER_OF_MINUTES_IN_A_DAY/meeting.duration)

    for p in meeting_participants:
        meeting_participant_slot = MeetingParticipantSlot.objects.filter(meeting_participant=p)
        best_slots = update_best_slots(meeting_participant_slot, best_slots)

    return render(request, 'response_page.html', {'best_slots': best_slots})