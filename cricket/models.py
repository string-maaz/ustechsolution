# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class RecordTimeStamp(models.Model):
    created_at=models.DateTimeField(auto_now=False,auto_now_add=True,blank=False,null=False) # while auto_now_add will save the date and time only when record is first created
    last_modified=models.DateTimeField(auto_now=True,auto_now_add=False) # auto_now will add the current time and date whenever field is saved.
    
    class Meta:
        abstract = True

class SoftDeletion(RecordTimeStamp):
    is_active = models.BooleanField(default = True)


    def delete(self):
        self.is_active = False
        self.save()
        return True

    class Meta:
        abstract = True


class Team(SoftDeletion):
    name = models.CharField(_("Name"), max_length=100, blank=True, db_index=True)
    logo_uri = models.CharField(_("Logo"), max_length=1000, blank=True)
    club_state = models.CharField(_("Club State"), max_length=100, blank=True, db_index=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __unicode__(self):
        return self.name

class Player(SoftDeletion):
    team = models.ForeignKey(Team, blank = False, null = False, related_name='team_players')
    firstname = models.CharField(_("Name"), max_length=50, blank=True, db_index=True)
    lastname = models.CharField(_("Name"), max_length=50, blank=True, db_index=True)
    image_uri = models.CharField(_("Player Image"), max_length=1000, blank=True)
    jersy_number = models.PositiveIntegerField(_("jersy_number"), default=0)
    country = models.CharField(_("Country"), max_length=100, blank=True, db_index=True)

    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")

    def __unicode__(self):
        return str(self.firstname)+' '+ str(self.lastname)

class PlayerHistory(SoftDeletion):
    player = models.ForeignKey(Player, blank = False, null = False, related_name='player_history')
    matches_played = models.PositiveIntegerField(_("Matches Played"), default=0)
    total_run = models.PositiveIntegerField(_("Matches Played"), default=0)
    highest_score = models.PositiveIntegerField(_("Highest Score"), default=0)
    fifties = models.PositiveIntegerField(_("Fifties"), default=0)
    hundreds = models.PositiveIntegerField(_("hundreds"), default=0)
    wickets = models.PositiveIntegerField(_("Wickets"), default=0)
    run_rate = models.FloatField(_("Run Rate"), default=0)
    strike_rate = models.FloatField(_("Strike Rate"), default=0)

    class Meta:
        verbose_name = _("PlayerHistory")
        verbose_name_plural = _("PlayerHistory")

    def __unicode__(self):
        return str(self.player)

match_status_options = (
    ('1', "Win"),
    ('2', "Draw"),
)

class Match(SoftDeletion):
    team1 = models.ForeignKey(Team, blank = False, null = False, related_name='team_1')
    team2 = models.ForeignKey(Team, blank = False, null = False, related_name='team_2')
    match_status = models.CharField(_("Match Status"), choices=match_status_options, max_length=2, default='2')
    winning_team = models.ForeignKey(Team, blank = True, null = True, related_name='winning_team')

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def __unicode__(self):
        return str(self.team1)+' vs ' +str(self.team2)

class MatchPoint(SoftDeletion):
    match = models.ForeignKey(Match, blank = False, null = False, related_name='match_point')
    team = models.ForeignKey(Team, blank = False, null = False, related_name='team_point')
    points = models.PositiveIntegerField(_("Points"), default=0)

    class Meta:
        verbose_name = _("MatchPoint")
        verbose_name_plural = _("MatchPoints")

    def __unicode__(self):
        return str(self.team)+' - '+str(self.points)
