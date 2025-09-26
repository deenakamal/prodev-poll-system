from rest_framework import serializers
from .models import Poll, Option, Vote


class OptionSerializer(serializers.ModelSerializer):
    """Serialize poll options with vote count."""
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['id', 'text', 'votes_count']

    def get_votes_count(self, obj):
        return obj.votes.count()


class PollSerializer(serializers.ModelSerializer):
    """Serialize poll with its options."""
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']


class VoteSerializer(serializers.ModelSerializer):
    """Serialize vote creation; user is read-only."""
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'user']
        read_only_fields = ['user']


class OptionUserSerializer(serializers.ModelSerializer):
    """Serialize option with user vote info and percentage."""
    user_voted = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['id', 'text', 'votes_count', 'user_voted', 'percentage']

    def get_user_voted(self, obj):
        user = self.context['request'].user
        return obj.votes.filter(user=user).exists()

    def get_percentage(self, obj):
        total_votes = sum(option.votes_count for option in obj.poll.options.all()) or 1
        return round((obj.votes_count / total_votes) * 100, 2)


class PollUserVoteSerializer(serializers.ModelSerializer):
    """Serialize poll with user-specific voting info."""
    options = OptionUserSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']
