from typing import Any
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DetailView, FormView, CreateView
from django.contrib.auth.models import User
from mbb.models import School, Player, PlayerSeason, UserProfile
from stats.models import MbbGameEspn, MbbStatlineEspn, MbbGameSref, MbbStatlineSref
from datetime import date
# Create your views here.

class MbbTemplateView(TemplateView):
    template_name = 'base_mbb.html'

class ListSchoolsView(ListView):
    model = School
    template_name = 'school_list.html'
    context_object_name = 'school_list'

class ListPlayersView(ListView):
    model = Player
    template_name = 'player_list.html'
    context_object_name = 'player_list'

class PlayerSeasonDetailView(DetailView):
    model = PlayerSeason

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

class LiveStatsListView(TemplateView):
    model = MbbStatlineEspn
    template_name = 'live_stats.html'
    context_object_name = 'stats_info'
    
    '''def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['games'] = MbbGameEspn.objects.filter(date=date.today())
        context['schools'] = School.objects.all()
        context['players'] = Player.objects.all()
        context['live_stats'] = MbbStatlineEspn.objects.filter(minutes=None)
        
        return context'''

class ListPlayerStatsView(ListView):
    model = MbbStatlineEspn
    template_name = 'mbb_stats.html'
    context_object_name = 'mbb_player_stats'

class GamesTodayListView(ListView):
    model = MbbGameEspn
    #template_name = 'games_today.html'
    context_object_name = 'games_today_espn'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = MbbGameEspn.objects.all()
        return context

class CreateUserFormView(CreateView):
    model = UserProfile
    #template_name = 'create_user.html'
    fields = ['tag_line']


def test_view(request):
    query = PlayerSeason.objects.filter()
    context = {'today': query}
    template = loader.get_template('today.html')
    return render(request, 'today.html', context)




#class PlayerDetailView(DetailView):
#    model = Player.objects.get(id=)
#
#    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#        context = super().get_context_data(**kwargs)
#        return context
