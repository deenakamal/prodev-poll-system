from django.urls import path
from .views import PollListView, VoteCreateView, UserVotedPollsListView, PollResultsView


urlpatterns = [
    path('', PollListView.as_view(), name='poll-list'),
    path('vote/', VoteCreateView.as_view(), name='vote-create'),
    path('my-votes/', UserVotedPollsListView.as_view(), name='user-voted-polls'),
    path('results/<int:pk>/', PollResultsView.as_view(), name='poll-results'),

    
]