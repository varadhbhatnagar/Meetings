from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import OrganiserForm, ParticipantForm, ResponseForm
from .models import Meeting, Participant, MeetingParticipant, MeetingParticipantSlot
from .util import get_feasible_slots, get_random_alphanumeric_string, get_slots, update_best_slots, NUMBER_OF_MINUTES_IN_A_DAY, flip_slots


def organiser_view(request):

    if request.method == 'GET':
        form = OrganiserForm()
        return render(request, 'organiser_page.html', {'form': form})

    else: #POST
        form = OrganiserForm(request.POST, request.FILES)
        if form.is_valid():

            organiser = Participant()
            organiser.contact = form.cleaned_data['organiser_contact_number']
            organiser.save()

            meeting = Meeting()
            meeting.meeting_hash = get_random_alphanumeric_string()
            meeting.organiser = organiser
            meeting.duration = form.cleaned_data['meeting_duration']
            meeting.date = form.cleaned_data['meeting_date']
            meeting.title = form.cleaned_data['meeting_agenda']
            meeting.save()

            meeting_participant = MeetingParticipant()
            meeting_participant.meeting = meeting
            meeting_participant.participant = organiser
            meeting_participant.save()

            message = 'New Meeting Created. \n\n Invite participants by sending link : /meeting/{}'.format(meeting.meeting_hash)
            message = message  + '\n\n Meeting Response can be found at : /response/{}'.format(meeting.meeting_hash)

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
        form = ParticipantForm(meeting_hash, request.POST, request.FILES)

        if form.is_valid():
            participant = Participant()
            participant.contact = form.cleaned_data['participant_contact_number']

            if Participant.objects.filter(contact = participant.contact).first() != None:
                message = 'You have already filled the form once. Cannnot fill again !'

            else:
                participant.save()

                meeting_participant = MeetingParticipant()
                meeting_participant.participant = participant
                meeting_participant.meeting = Meeting.objects.get(meeting_hash = form.cleaned_data['meeting_hash'])
                meeting_participant.save()

                if form.cleaned_data['availability'] == '2':
                    form.cleaned_data['slot'] = flip_slots(form.cleaned_data['slot'], int(NUMBER_OF_MINUTES_IN_A_DAY/int(meeting_participant.meeting.duration)))

                for slot in form.cleaned_data['slot']:
                    meeting_participant_slot = MeetingParticipantSlot()
                    meeting_participant_slot.meeting_participant = meeting_participant
                    meeting_participant_slot.slot = slot
                    meeting_participant_slot.save()

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

    best_slots = [0] * int(NUMBER_OF_MINUTES_IN_A_DAY/int(meeting.duration))

    for p in meeting_participants:
        meeting_participant_slot = MeetingParticipantSlot.objects.filter(meeting_participant=p)
        best_slots = update_best_slots(meeting_participant_slot, best_slots)

    best_slots = get_feasible_slots(best_slots)
    bs = ''
    slots = get_slots(int(meeting.duration))
    for b in range(len(best_slots)):
        bs += slots[b][1]
        bs += ", "

    initial = {'meeting_agenda': meeting.title, 'organiser_contact_number': meeting.organiser.contact, 'meeting_hash': meeting.meeting_hash, 'best_slots': bs, 'response_count': len(meeting_participants)}
    form = ResponseForm(initial = initial)
    return render(request, 'response_page.html', {'form': form})