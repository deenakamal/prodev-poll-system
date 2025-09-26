from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer, PollUserVoteSerializer
from .pagination import PollPagination
from .utils import get_poll_results
from rest_framework.response import Response
from .utils import invalidate_poll_cache


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

    def create(self, request, *args, **kwargs):
        poll_id = request.data.get("poll")
        user = request.user

        if Vote.objects.filter(poll_id=poll_id, user=user).exists():
            return Response(
                {"detail": "You have already voted in this poll."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        vote = serializer.save(user=self.request.user)

        option = vote.option
        option.votes_count = option.votes.count()
        option.save()

        invalidate_poll_cache(vote.poll.id)
        
        
class UserVotedPollsListView(generics.ListAPIView):
    serializer_class = PollUserVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        polls = Poll.objects.filter(votes__user=self.request.user, is_deleted=False).distinct()
        for poll in polls:
            for option in poll.options.all():
                option.votes_count = option.votes.count()
        return polls


class PollResultsView(generics.RetrieveAPIView):
    queryset = Poll.objects.filter(is_deleted=False)
    serializer_class = PollUserVoteSerializer
    permission_classes = [permissions.AllowAny]  # or IsAuthenticated if you want to restrict

    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        results = get_poll_results(poll.id)  # from cache or db
        data = {
            "poll": poll.question,
            "expires_at": poll.expires_at,
            "results": results
        }
        return Response(data)
