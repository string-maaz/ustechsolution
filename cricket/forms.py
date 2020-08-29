from django.forms import ModelForm, Form
from cricket.models import *
from django import forms
import datetime

class TeamForm(ModelForm):
    class Meta:
        model = Team
        exclude = ['is_active', 'created_at', 'last_modified']
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        for field in self: 
            field.field.widget.attrs['class'] = 'form-control'
            

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        exclude = ['is_active', 'created_at', 'last_modified']     
    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        for field in self: 
            field.field.widget.attrs['class'] = 'form-control'


class MatchForm(ModelForm):
    class Meta:
        model = Match
        exclude = ['is_active']
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        for field in self: 
            field.field.widget.attrs['class'] = 'form-control'

class MatchPointForm(ModelForm):
    class Meta:
        model = MatchPoint
        exclude = ['is_active']
    def __init__(self, *args, **kwargs):
        super(MatchPointForm, self).__init__(*args, **kwargs)
        for field in self: 
            field.field.widget.attrs['class'] = 'form-control'