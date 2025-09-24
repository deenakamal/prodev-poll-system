from rest_framework import serializers
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'votes_count']

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'user']
        read_only_fields = ['user']
        


class OptionUserSerializer(serializers.ModelSerializer):
    user_voted = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['id', 'text', 'votes_count', 'user_voted', 'percentage']

    def get_user_voted(self, obj):
        user = self.context['request'].user
        return obj.votes.filter(user=user).exists()

    def get_percentage(self, obj):
        total_votes = sum(option.votes_count for option in obj.poll.options.all())
        if total_votes == 0:
            return 0
        return round((obj.votes_count / total_votes) * 100, 2)


class PollUserVoteSerializer(serializers.ModelSerializer):
    options = OptionUserSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_at', 'expires_at', 'options']
