from django.core.cache import cache
from .models import Poll, Vote


def get_poll_results(poll_id):
    """
    Retrieve poll results with vote counts and percentages for each option.
    Uses cache to improve performance, recalculates if not cached.
    """
    key = f'poll_results_{poll_id}'
    results = cache.get(key)

    if results is None:
        # Fetch poll with options and prefetch votes
        poll = Poll.objects.prefetch_related('options__votes').get(id=poll_id)

        # Correct total votes: sum of all votes across options
        total_votes = sum(option.votes.count() for option in poll.options.all()) or 0

        results = {}
        for option in poll.options.all():
            count = option.votes.count()
            percentage = (count / total_votes * 100) if total_votes else 0
            results[option.text] = {
                "count": count,
                "percentage": round(percentage, 2)
            }

        # Cache results for 60 seconds
        cache.set(key, results, timeout=60)

    return results

def invalidate_poll_cache(poll_id):
    """
    Delete poll results from cache. Call this after a vote is created.
    """
    key = f'poll_results_{poll_id}'
    cache.delete(key)
