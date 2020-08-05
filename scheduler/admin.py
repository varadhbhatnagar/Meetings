from django.contrib import admin

from .models import Participant, Meeting, MeetingParticipant, MeetingParticipantSlot

admin.site.register(Participant)
admin.site.register(Meeting)
admin.site.register(MeetingParticipant)
admin.site.register(MeetingParticipantSlot)
