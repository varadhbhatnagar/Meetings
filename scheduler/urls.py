from django.conf.urls import url
from .import views

urlpatterns = [
    url('organiser/', views.organiser_view, name="organiser_page"),
    url(r'meeting/(?P<meeting_hash>\w+)/$', views.participant_view, name="participant_page"),
    url(r'response/(?P<meeting_hash>\w+)/$', views.response_view, name="response_page")
]

