import cache


class Device:

    def communicate(self):
        pass




class BaseStation(Device):
    def __init__(self, cache_capacity, caching_algorithm, range):
        self.cache = cache.Cache(cache_capacity, caching_algorithm)
        self.range = range



class Satellite(Device):
    def __init__(self, cache_capacity, caching_algorithm, distance):
        self.cache = cache.Cache(cache_capacity, caching_algorithm)




class Mobile(Device):
    def __init__(self, cache_capacity, caching_algorithm, range):
        self.cache = cache.Cache(cache_capacity, caching_algorithm)
        self.range = range

