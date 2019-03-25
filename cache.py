
class Cache:
    def __init__(self, cache_capacity, caching_algorithm):
        self.cache = []
        self.capacity = cache_capacity
        self.algorithm = caching_algorithm


    # Return true if cache contains the content
    def contains(self, content):
        return True

    def is_full(self):
        return self.capacity == 0

    # Uses LRU page replacement algorithm when a new content has came
    def LRU(self, new_content):
        pass

    # Uses MLPLRU page replacement algorithm when a new content has came
    def MLPLRU(self, new_content):
        pass

    # Uses Cache_me_Cache page replacement algorithm when a new content has came
    def Cache_Me_Cache(self, new_content):
        pass


    def new_content(self, content):
        if self.algorithm == "LRU":
            self.LRU(content)
        elif self.algorithm == "MLPLRU":
            self.MLPLRU(content)
        elif self.algorithm == "Cache-Me-Cache":
            self.Cache_Me_Cache(content)

