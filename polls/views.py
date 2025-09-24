from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer
from .pagination import PollPagination
from .utils import get_poll_results

class PollListView(generics.ListAPIView):
    queryset = Poll.objects.filter(is_deleted=False)
    serializer_class = PollSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_by']
    search_fields = ['question']
    ordering_fields = ['created_at', 'expires_at', 'question']
    ordering = ['-created_at']
    pagination_class = PollPagination


class VoteCreateView(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        vote = serializer.save(user=self.request.user)

        
        option = vote.option
        option.votes_count = option.votes.count()
        option.save()

        
        from .utils import get_poll_results
        get_poll_results(vote.poll.id)
