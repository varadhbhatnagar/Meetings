from django.db import models

class Participant(models.Model):
    contact = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

class Meeting(models.Model):
    meeting_hash = models.CharField(max_length = 100, primary_key = True)
    organiser = models.ForeignKey(Participant, on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.CharField(max_length=10)
    title = models.CharField(max_length=100)

class MeetingParticipant(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

class MeetingParticipantSlot(models.Model):
    meeting_participant = models.ForeignKey(MeetingParticipant, on_delete=models.CASCADE)
    slot = models.CharField(max_length=10)


