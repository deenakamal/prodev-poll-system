from django.core.cache import cache
from .models import Poll

def get_poll_results(poll_id):
    """
    Retrieve poll results with count and percentage for each option.
    Uses cache to improve performance, recalculates if not cached.
    """
    key = f'poll_results_{poll_id}'
    results = cache.get(key)

    if results is None:
        poll = Poll.objects.prefetch_related('options__votes').get(id=poll_id)
        total_votes = poll.votes.count()
        results = {}

        for option in poll.options.all():
            count = option.votes.count()
            percentage = (count / total_votes * 100) if total_votes else 0
            results[option.text] = {
                "count": count,
                "percentage": round(percentage, 2)
            }

        cache.set(key, results, timeout=60)  # cache results for 60 seconds

    return results

def invalidate_poll_cache(poll_id):
    """
    Delete poll results from cache. Call this after a vote is created.
    """
    key = f'poll_results_{poll_id}'
    cache.delete(key)
