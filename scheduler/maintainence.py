from .models import Meeting, MeetingParticipant
from datetime import date

def db_cleaner():

    today = date.today()
    print("DB Maintainence started for {}".format(today))

    outdated_meetings = Meeting.objects.filter(date__lt=today)
    print("Deleted {} Meetings".format(len(outdated_meetings)))

    outdated_meetings.delete()