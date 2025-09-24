from django.core.cache import cache
from .models import Poll

def get_poll_results(poll_id):
    key = f'poll_results_{poll_id}'
    results = cache.get(key)
    if results is None:
        poll = Poll.objects.prefetch_related('options').get(id=poll_id)
        results = {opt.text: opt.votes_count for opt in poll.options.all()}
        cache.set(key, results, timeout=60)
    return results
