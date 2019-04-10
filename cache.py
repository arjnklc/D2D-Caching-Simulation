import parameters


class Cache:
    def __init__(self, cache_capacity, caching_algorithm):
        self.cache = []
        self.capacity = cache_capacity / parameters.CONTENT_SIZE
        self.algorithm = caching_algorithm

    def contains(self, content):
        return content in self.cache

    def clear(self):
        self.cache = []

    def is_full(self):
        return self.capacity == len(self.cache)


    # Uses LRU page replacement algorithm when a new content has came
    def LRU(self, new_content):
        if self.contains(new_content):
            index = self.cache.index(new_content)
            del self.cache[index]
        if self.is_full():
            del self.cache[-1]  # Remove the last element if cache is full

        self.cache.insert(0, new_content)   # insert new content to the head

    # Uses MLPLRU page replacement algorithm when a new content has arrived
    def MLPLRU(self, new_content):
        pass

    # Uses Cache_me_Cache page replacement algorithm when a new content has arrived
    def Cache_Me_Cache(self, new_content):
        pass

    def new_content(self, content):
        if self.algorithm == "LRU":
            self.LRU(content)
        elif self.algorithm == "MLPLRU":
            self.MLPLRU(content)
        elif self.algorithm == "Cache-Me-Cache":
            self.Cache_Me_Cache(content)

