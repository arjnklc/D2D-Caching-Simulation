import parameters
import abc
import math


class Cache:
    @abc.abstractmethod
    def clear(self):
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
        self.capacity_for_each_level = math.ceil(self.capacity / 3)
        self.lvl1, self.lvl2, self.lvl3 = [], [], []

        self.threshold = 2  # Xi

        self.puanlar = {}

    def contains(self, content):
        return content in self.lvl1 or content in self.lvl2 or content in self.lvl3

    def clear(self):
        self.lvl1, self.lvl2, self.lvl3 = [], [], []
        self.puanlar = {}

    def is_level_full(self, i):
        return self.capacity_for_each_level == len(self.get_cache_level(i))

    def get_level_of_content(self, content):
        if content in self.lvl1:
            return 1
        elif content in self.lvl2:
            return 2
        elif content in self.lvl3:
            return 3

    def get_cache_level(self, i):
        if i == 1:
            return self.lvl1
        elif i == 2:
            return self.lvl2
        elif i == 3:
            return self.lvl3

    def new_content(self, new_content):
        if self.contains(new_content):
            i = self.get_level_of_content(new_content)
            self.puanlar[new_content] += 1
            if self.puanlar[new_content] < self.threshold:
                # move the content to the header of the cache level
                lvli = self.get_cache_level(i)
                lvli.insert(0, lvli.pop(lvli.index(new_content)))
            else:
                if i == 1:
                    # move the content to the header of the cache level
                    self.lvl1.insert(0, self.lvl1.pop(self.lvl1.index(new_content)))
                    self.puanlar[new_content] += 1

                elif not self.is_level_full(i-1):
                    # remove the content from cache level i and insert it to the cache level i-1
                    self.get_cache_level(i).remove(new_content)
                    self.get_cache_level(i-1).insert(0, new_content)
                    self.puanlar[new_content] = 0

                elif self.is_level_full(i-1):
                    higher_level = self.get_cache_level(i-1)
                    current_level = self.get_cache_level(i)
                    downgraded_content = higher_level[-1]  # last element of cache level
                    del higher_level[-1]
                    current_level.remove(new_content)  # Remove from current level
                    higher_level.insert(0, new_content)  # insert to the higher level (upgrade)
                    self.get_cache_level(i).insert(0, downgraded_content)  # insert to head of lower cache level
                    self.puanlar[downgraded_content] = 0
                    self.puanlar[new_content] = 0

        else:
            if self.is_level_full(3):
                removed_content = self.lvl3[-1]
                del self.lvl3[-1]  # Remove the last element of level 3
                del self.puanlar[removed_content]

            self.lvl3.insert(0, new_content)  # insert new content to the head of level 3
            self.puanlar[new_content] = 1


class Cache_Me_Cache(Cache):
    def __init__(self, cache_capacity):
        self.cache = {}     # Dictionary: content -> score
        self.capacity = cache_capacity / parameters.CONTENT_SIZE
        self.score_decrease = 0.3

        self.score_increase = self.capacity
        self.threshold = 0.5 * self.capacity  # ????

    def contains(self, content):
        return content in self.cache.keys()

    def clear(self):
        self.cache = {}

    def is_full(self):
        return self.capacity == len(self.cache)

    # delete the lowest scored content if it's score is below threshold
    def delete_content_if_possible(self):
        if min(self.cache.values()) < self.threshold:
            deleted = min(self.cache, key=lambda k: self.cache[k])
            del self.cache[deleted]

    def decrease_all_scores(self, amount):
        for content, score in self.cache.items():
            self.cache[content] -= amount

    def new_content(self, new_content):

        self.decrease_all_scores(self.score_decrease)

        if self.contains(new_content):
            self.cache[new_content] += self.score_increase
            # indexini bul skoru arttır
            return
        else:
            if self.is_full():
                self.delete_content_if_possible()
            # Mümkünse en az popüler contenti sil ve sildiysen yeni contenti ekle
            if not self.is_full():
                self.cache[new_content] = self.score_increase
