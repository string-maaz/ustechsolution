from django.conf.urls import url,include
from cricket.views import *
urlpatterns = [
    url(r'^team/$',TeamView.as_view(),name='team'),
    url(r'^player/$',PlayerView.as_view(),name='player'),
    url(r'^match/$',MatchView.as_view(),name='match'),
    url(r'^matchpoint/$',MatchPointView.as_view(),name='matchpoint'),
    url(r'^team_match_point/$',SingleTeamMatchPointView.as_view(),name='team_match_point'),
    ]