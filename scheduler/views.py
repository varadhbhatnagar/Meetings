from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import OrganiserForm, ParticipantForm, ResponseForm
from .models import Meeting, Participant, MeetingParticipant, MeetingParticipantSlot
from .util import get_most_suitable_slots, get_hash, update_current_suitable_slots, flip_slots, get_slot_choices


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
            meeting.organiser = organiser
            meeting.duration = form.cleaned_data['meeting_duration']
            meeting.date = form.cleaned_data['meeting_date']
            meeting.title = form.cleaned_data['meeting_agenda']
            meeting.meeting_hash = get_hash()
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

            if MeetingParticipant.objects.filter(participant = participant).first() != None:
                message = 'You have already filled the form once. Cannnot fill again !'

            else:
                participant.save()

                meeting_participant = MeetingParticipant()
                meeting_participant.participant = participant
                meeting_participant.meeting = Meeting.objects.filter(meeting_hash = form.cleaned_data['meeting_hash']).first()
                meeting_participant.save()

                if form.cleaned_data['availability'] == '2':
                    _, slot_count = get_slot_choices(int(meeting_participant.meeting.duration))
                    form.cleaned_data['slot'] = flip_slots(form.cleaned_data['slot'], slot_count)

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
    
    meeting = Meeting.objects.filter(meeting_hash = meeting_hash).first()
    meeting_participants = MeetingParticipant.objects.filter(meeting=meeting)
    _, slot_count = get_slot_choices(int(meeting.duration))

    current_suitable_slots = [0] * slot_count

    for participant in meeting_participants:
        meeting_participant_slot = MeetingParticipantSlot.objects.filter(meeting_participant=participant)
        current_suitable_slots = update_current_suitable_slots(meeting_participant_slot, current_suitable_slots)

    most_suitable_slots = get_most_suitable_slots(current_suitable_slots, limit = 8)
    most_suitable_slots_string = ''
    slot_choices, _ = get_slot_choices(int(meeting.duration))

    for slot in most_suitable_slots:
        most_suitable_slots_string += slot_choices[slot][1]
        most_suitable_slots_string += "\n"

    initial = {'meeting_agenda': meeting.title, 'organiser_contact_number': meeting.organiser.contact, 'meeting_hash': meeting.meeting_hash, 'best_slots': most_suitable_slots_string, 'response_count': len(meeting_participants)}
    form = ResponseForm(initial = initial)
    return render(request, 'response_page.html', {'form': form})