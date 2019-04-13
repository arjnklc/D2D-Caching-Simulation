import parameters
import abc


class Cache:

    @abc.abstractmethod
    def clear(self):
        return

    @abc.abstractmethod
    def is_full(self):
        return

    @abc.abstractmethod
    def contains(self, content):
        return

    @abc.abstractmethod
    def new_content(self, new_content):
        return


class LRU_Cache(Cache):
    def __init__(self, cache_capacity):
        self.cache = []
        self.capacity = cache_capacity / parameters.CONTENT_SIZE

    def contains(self, content):
        return content in self.cache

    def clear(self):
        self.cache = []

    def is_full(self):
        return self.capacity == len(self.cache)

    def new_content(self, new_content):
        if self.contains(new_content):
            index = self.cache.index(new_content)
            del self.cache[index]
        if self.is_full():
            del self.cache[-1]  # Remove the last element if cache is full

        self.cache.insert(0, new_content)   # insert new content to the head


class MLPLRU_Cache(Cache):
    def __init__(self, cache_capacity):
        self.capacity = cache_capacity / parameters.CONTENT_SIZE
        self.capacity_for_each_level = self.capacity / 3
        self.lvl1, self.lvl2, self.lvl3 = [], [], []

        self.threshold = 2  # Xi



    def contains(self, content):
        return content in self.cache.keys()

    def clear(self):
        self.cache = {}

    def is_full(self):
        return self.capacity == len(self.cache)



    def new_content(self, new_content):

        pass


class Cache_Me_Cache(Cache):
    def __init__(self, cache_capacity):
        self.cache = {}     # Dictionary: content -> score
        self.capacity = cache_capacity / parameters.CONTENT_SIZE
        self.score_decrease = 1

        self.score_increase = self.capacity
        self.threshold = 0.1 * self.capacity  # ????


    def contains(self, content):
        return content in self.cache.keys()

    def clear(self):
        self.cache = {}

    def is_full(self):
        return self.capacity == len(self.cache)

    def delete_content_if_possible(self):
        for content, score in self.cache.items():
            if score < self.threshold:
                del self.cache[content]
                return

    def decrease_all_scores(self, num):
        for content, score in self.cache.items():
            self.cache[content] -= num

    def new_content(self, new_content):

        self.decrease_all_scores(self.score_decrease)

        if self.contains(new_content):
            self.cache[new_content] += self.score_increase
            # indexini bul skoru arttır
            return
        else:
            self.delete_content_if_possible()
            # Mümkünse en az popüler contenti sil ve sildiysen yeni contenti ekle
            if not self.is_full():
                self.cache[new_content] = self.score_increase







