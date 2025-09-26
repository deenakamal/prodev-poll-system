from django.contrib import admin
from .models import Poll, Option, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """
    Admin view for Poll model.
    Shows basic info, creator, expiration, and total votes.
    """
    list_display = ("id", "question", "created_by", "created_at", "expires_at", "is_deleted", "total_votes")
    list_filter = ("is_deleted", "created_at", "expires_at", "created_by")
    search_fields = ("question", "created_by__username")
    ordering = ("-created_at",)

    def total_votes(self, obj):
        """Calculate the total number of votes for this poll."""
        return obj.votes.count()
    total_votes.short_description = "Total Votes"  # Column title in admin


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """
    Admin view for Option model.
    Shows text, related poll, and votes count.
    """
    list_display = ("id", "text", "poll", "votes_count")
    list_filter = ("poll",)
    search_fields = ("text", "poll__question")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Admin view for Vote model.
    Shows poll, option, user, and created_at.
    """
    list_display = ("id", "poll", "option", "user", "created_at")
    list_filter = ("poll", "option", "user")
    search_fields = ("user__username", "poll__question", "option__text")
    ordering = ("-created_at",)
