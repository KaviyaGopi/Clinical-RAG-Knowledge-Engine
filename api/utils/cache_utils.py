from django.core.cache import cache
from api.exceptions import ApplicationError

def cache_data(key, value, timeout=3600):
    try:
        cache.set(key, value, timeout)
    except Exception as e:
        raise ApplicationError(f"Failed to cache data for key '{key}': {e}", status_code=500)

def get_cached_data(key):
    try:
        data = cache.get(key)
        if data is None:
            raise ApplicationError(f"No cached data found for key '{key}'", status_code=404)
        return data
    except Exception as e:
        raise ApplicationError(f"Failed to retrieve cached data for key '{key}': {e}", status_code=500)

def delete_cached_data(key):
    try:
        cache.delete(key)
    except Exception as e:
        raise ApplicationError(f"Failed to delete cached data for key '{key}': {e}", status_code=500)