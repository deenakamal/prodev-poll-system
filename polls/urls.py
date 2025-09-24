from django.urls import path
from .views import PollListView, VoteCreateView


urlpatterns = [
    path('', PollListView.as_view(), name='poll-list'),
    path('vote/', VoteCreateView.as_view(), name='vote-create'),
    
]