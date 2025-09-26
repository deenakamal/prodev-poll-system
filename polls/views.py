from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer, PollUserVoteSerializer
from .pagination import PollPagination
from .utils import get_poll_results, invalidate_poll_cache
from rest_framework.response import Response


class PollListView(generics.ListAPIView):
    """List all polls with filtering, searching, ordering, and pagination."""
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
    """Create a vote ensuring user votes only once per poll."""
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        poll_id = request.data.get("poll")
        option_id = request.data.get("option")
        user = request.user

        # Prevent double voting
        if Vote.objects.filter(poll_id=poll_id, user=user).exists():
            return Response({"detail": "You have already voted in this poll."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Validate option belongs to poll
        from .models import Poll
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"detail": "Poll not found."}, status=status.HTTP_404_NOT_FOUND)

        if not poll.options.filter(id=option_id).exists():
            return Response({"detail": "Invalid option for this poll."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


class UserVotedPollsListView(generics.ListAPIView):
    """List polls that the current user has voted on."""
    serializer_class = PollUserVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        polls = Poll.objects.filter(votes__user=self.request.user, is_deleted=False).distinct()

        # Update vote counts and percentages for each option
        for poll in polls:
            total_votes = sum(option.votes.count() for option in poll.options.all()) or 1
            for option in poll.options.all():
                option.votes_count = option.votes.count()
                option.percentage = round((option.votes_count / total_votes) * 100, 2)
                option.user_voted = option.votes.filter(user=self.request.user).exists()

        return polls


class PollResultsView(generics.RetrieveAPIView):
    """Retrieve poll results."""
    queryset = Poll.objects.filter(is_deleted=False)
    serializer_class = PollUserVoteSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        results = get_poll_results(poll.id)
        data = {
            "poll": poll.question,
            "expires_at": poll.expires_at,
            "results": results
        }
        return Response(data)
