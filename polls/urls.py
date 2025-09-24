from django.urls import path
from .views import PollListView, VoteCreateView, UserVotedPollsListView


urlpatterns = [
    path('', PollListView.as_view(), name='poll-list'),
    path('vote/', VoteCreateView.as_view(), name='vote-create'),
      path('my-votes/', UserVotedPollsListView.as_view(), name='user-voted-polls'),
    
]