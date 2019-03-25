
class Cache:
    def __init__(self, cache_capacity, caching_algorithm):
        self.capacity = cache_capacity
        self.algorithm = caching_algorithm


    # TODO
    def contains(self, content):
        return True

    def is_full(self):
        return self.capacity == 0

    def LRU(self, new_content):
        pass

    def MLPLRU(self, new_content):
        pass

    def Cache_Me_Cache(self, new_content):
        pass



    def new_content(self, content):
        if self.algorithm == "LRU":
            self.LRU(content)
        elif self.algorithm == "MLPLRU":
            self.MLPLRU(content)
        elif self.algorithm == "Cache-Me-Cache":
            self.Cache_Me_Cache(content)

