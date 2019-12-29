from falcon_caching import Cache

# Setup the cache instance
cache = Cache(
    config=
    {
        # Sets management strategy of the cache
        'CACHE_EVICTION_STRATEGY': 'time-based',  
        # Sets type of cache ('null' sets no cache, used for development and unit test)
        # A prodcution environment should use onother type of cache such as 'simple.'
        'CACHE_TYPE': 'null' 
    })