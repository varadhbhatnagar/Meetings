# Generated by Django 3.1 on 2020-08-05 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('meeting_hash', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('duration', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('contact', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingParticipantSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=10)),
                ('meeting_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.meetingparticipant')),
            ],
        ),
        migrations.AddField(
            model_name='meetingparticipant',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.participant'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='organiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduler.participant'),
        ),
    ]