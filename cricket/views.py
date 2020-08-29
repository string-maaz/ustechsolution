# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from cricket.forms import *
import json
from django.db.models import Sum


class USTechSolutionFormView(FormView):
    template_name = 'cricket/form.html' # Form Template
    view_template_name = 'cricket/show_all.html'
    form_class = None
    model = None
    url_name = ''

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')
        data = {}   
        if action == 'add' or action == 'edit':
            return super(USTechSolutionFormView,self).get(request,*args,**kwargs)
        elif action == 'delete':
            object_id = request.GET.get('pk')
            try:
                obj = self.get_model().objects.get(id = object_id)
                obj.is_active = False
                obj.save()
                data['message'] = 'Succesfully Deleted'
            except Exception as e:
                print 'Error',e
        filter_dict = {}
        for key in request.GET.iterkeys():
            filter_dict[key] = request.GET.get(key)
        if filter_dict:
            all_data = self.get_model().objects.filter(is_active=True).filter(**filter_dict)
        else:
            all_data = self.get_model().objects.filter(is_active=True)
        fields = [field for field in self.get_form().fields]
        data['all_data'] = all_data
        data['field_names'] = fields
        data['url_name'] = self.url_name
        data['form_name'] = self.form_name
        return render(request,self.view_template_name,data)


    def get_model(self):
        return self.model


    def get_form_kwargs(self):
        kwargs = super(USTechSolutionFormView,self).get_form_kwargs()
        if self.request.GET.get('action') == 'edit':
            kwargs['instance'] = self.get_instance()
        return kwargs


    def get_context_data(self, **kwargs):
        kwargs['success_url'] = self.success_url
        kwargs['form_name'] = self.form_name
        return super(USTechSolutionFormView,self).get_context_data(**kwargs)


    def get_instance(self):
        pk = self.request.GET.get('pk')
        return self.get_model().objects.get(id = pk)


    def form_valid(self, form):
        form.save()
        return super(USTechSolutionFormView,self).form_valid(form)

class TeamView(USTechSolutionFormView):
    form_class = TeamForm
    model = Team
    url_name = 'team'
    success_url = '/cricket/team/'
    form_name = 'Add New Team'

class PlayerView(USTechSolutionFormView):
    form_class = PlayerForm
    model = Player
    url_name = 'player'
    success_url = '/cricket/team/'
    form_name = 'Add New Player'

class MatchView(USTechSolutionFormView):
    form_class = MatchForm
    model = Match
    url_name = 'match'
    success_url = '/cricket/match/'
    form_name = 'Add New Match'

    def form_valid(self, form):
        match_form = form.save(commit=False)
        if match_form.winning_team and not match_form.winning_team in [match_form.team1, match_form.team2]:
            form.add_error("winning_team","winning team must be from team 1 or team 2")
            return self.form_invalid(form)
        elif match_form.match_status == '2':
            form.add_error("match_status","if match is draw no team can win")
            return self.form_invalid(form)
        match_form.save()
        return super(MatchView,self).form_valid(form)

class MatchPointView(USTechSolutionFormView):
    form_class = MatchPointForm
    model = MatchPoint
    url_name = 'matchpoint'
    success_url = '/cricket/matchpoint/'
    form_name = 'Add New MatchPoint'

class SingleTeamMatchPointView(TemplateView):
    template_name = 'cricket/team_points.html'
    post_template_name = 'cricket/team_points_list.html'


    def get_context_data(self, **kwargs):
        request_type = self.request.method
        if request_type == 'GET':
            kwargs['teams'] = Team.objects.filter(is_active = True)
        elif request_type == 'POST':
            team_id = int(self.request.POST.get('team'))
            # print 'team id ',team_id
            kwargs['matchpoints'] = MatchPoint.objects.filter(team_id = team_id, is_active = True).order_by('id')
            total_points = MatchPoint.objects.filter(team_id = team_id, is_active = True).aggregate(Sum('points'))
            print total_points
            if 'points__sum' in total_points:
                total_points = total_points['points__sum']
                kwargs['total_points'] = total_points
        return super(SingleTeamMatchPointView,self).get_context_data(**kwargs)


    def get_template_names(self):
        if self.template_name is None:
                raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        elif self.request.method == 'GET':
            return [self.template_name]
        elif self.request.method == 'POST':
            return [self.post_template_name]


    def post(self,request,*args,**kwargs):
        context = self.get_context_data(**kwargs)
        # print context
        data = {}
        data['html'] = render_to_string(self.get_template_names()[0],context)
        data['team'] = self.request.POST.get('team')
        return HttpResponse(json.dumps(data),content_type="application/json")


def dashboard(request):
    team_count = Team.objects.filter(is_active = True).count()
    player_count =  Player.objects.filter(is_active = True).count()
    match_count =  Match.objects.filter(is_active = True).count()
    data= {"team_count":team_count,"player_count":player_count,"match_count":match_count}
    # print data
    return render(request,'base_templates/layout/dashboard.html',{"data":data})


