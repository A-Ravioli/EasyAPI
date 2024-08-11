import redis
import memcache


class CacheService:
    def __init__(self, provider, **credentials):
        self.provider = provider
        if provider == "redis":
            self.client = redis.Redis(**credentials)
        elif provider == "memcached":
            self.client = memcache.Client(credentials["servers"], debug=0)
        else:
            raise ValueError("Unsupported caching provider")

    def set(self, key, value, expiration=3600):
        """
        Set a value in the cache with an optional expiration time.
        """
        if self.provider == "redis":
            self.client.set(key, value, ex=expiration)
        elif self.provider == "memcached":
            self.client.set(key, value, time=expiration)

    def get(self, key):
        """
        Get a value from the cache by its key.
        """
        return self.client.get(key)

    def delete(self, key):
        """
        Delete a value from the cache by its key.
        """
        self.client.delete(key)

    def flush(self):
        """
        Flush all data from the cache.
        """
        if self.provider == "redis":
            self.client.flushall()
        elif self.provider == "memcached":
            self.client.flush_all()
