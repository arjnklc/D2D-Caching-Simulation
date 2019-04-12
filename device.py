import cache


class Device:
    def set_cache(self, cache_capacity, caching_algorithm):
        if caching_algorithm == "LRU":
            self.cache = cache.LRU_Cache(cache_capacity)
        elif caching_algorithm == "MLPLRU":
            self.cache = cache.MLPLRU_Cache(cache_capacity)
        elif caching_algorithm == "Cache-Me-Cache":
            self.cache = cache.Cache_Me_Cache(cache_capacity)


class BaseStation(Device):
    def __init__(self, cache_capacity, caching_algorithm, range):
        self.range = range
        self.set_cache(cache_capacity, caching_algorithm)


class Satellite(Device):
    def __init__(self, cache_capacity, caching_algorithm, distance):
        self.distance = distance
        self.set_cache(cache_capacity, caching_algorithm)




class Mobile(Device):
    def __init__(self, id, cache_capacity, caching_algorithm, range):
        self.id = id
        self.range = range
        self.set_cache(cache_capacity, caching_algorithm)


