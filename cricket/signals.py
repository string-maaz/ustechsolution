from __future__ import unicode_literals

from django.dispatch import receiver,Signal
from django.db.models.signals import post_save
from cricket.models import *

@receiver([post_save],sender=Match)
def update_points_table(sender, instance, created, **kwargs):
	team_1 = instance.team1
	team_2 = instance.team2
	match_status = instance.match_status
	winning_team = instance.winning_team
	team_1_point, is_created = MatchPoint.objects.get_or_create(match = instance, team = team_1)
	team_2_point, is_created = MatchPoint.objects.get_or_create(match = instance, team = team_2)
	if match_status == '2':
		team_1_point.points = 1
		team_2_point.points = 1
	elif winning_team:
		if winning_team == team_1:
			team_1_point.points = 4
			team_2_point.points = 2
		else:
			team_2_point.points = 4
			team_1_point.points = 2
	elif not instance.is_active:
		team_1_point.is_active = False
		team_2_point.is_active = False
	team_1_point.save()
	team_2_point.save()



