from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Poll(models.Model):
    """Poll model with soft delete and optional expiration."""
    question = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='polls',
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['expires_at']),
        ]


class Option(models.Model):
    """Option belonging to a poll with vote count."""
    poll = models.ForeignKey(Poll, related_name="options", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    votes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.text} ({self.poll.question})"

    class Meta:
        indexes = [
            models.Index(fields=['poll']),
        ]


class Vote(models.Model):
    """Vote by a user for a specific option in a poll."""
    poll = models.ForeignKey(Poll, related_name="votes", on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name="votes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("poll", "user")
        indexes = [
            models.Index(fields=['poll']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.option.text}"
