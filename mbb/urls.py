from django.urls import path
from mbb.views import ListSchoolsView, MbbTemplateView, LiveStatsListView, CreateUserFormView, GamesTodayListView, test_view

urlpatterns = [
    path('', MbbTemplateView.as_view(), name='mbb'),
    path('schools/', ListSchoolsView.as_view(), name='schools'),
    path('stats/', LiveStatsListView.as_view(), name='live_stats'),
    path('new-user/', CreateUserFormView.as_view(), name='create-user'),
    path('today/', test_view, name='games_today'),
]