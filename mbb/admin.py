from django.contrib import admin
from mbb.models import School, Conference, Team, UserProfile, FantasyLeague, FantasyTeam

# Register your models here.
admin.site.register(School)
admin.site.register(Conference)
admin.site.register(Team)
admin.site.register(UserProfile)
admin.site.register(FantasyLeague)
admin.site.register(FantasyTeam)