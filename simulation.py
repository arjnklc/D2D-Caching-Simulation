import terrain
import device
import content
import random
import plotter

from parameters import *


class Simulator:

    def __init__(self):
        self.terrestrial = terrain.Terrain(TERRAIN_SIZE)

        self.place_base_station()
        self.place_satellite()
        self.place_mobiles_randomly(NUMBER_OF_USERS)

        # Generate content with zipf distribution
        self.contents = content.generate_zipf_content(NUMBER_OF_CONTENTS, CONTENT_SIZE, ZIPF_PARAMETER)

    def place_base_station(self):
        base_station = device.BaseStation(BASE_STATION_CACHE_CAPACITY, "LRU", BASE_STATION_RANGE)
        base_station.x = int(TERRAIN_SIZE / 2)
        base_station.y = int(TERRAIN_SIZE / 2)  # Located in center of terrain
        self.terrestrial.add_base_station(base_station)

    def place_satellite(self):
        satellite = device.Satellite(SATELLITE_CACHE_CAPACITY, "LRU", SATELLITE_DISTANCE)
        self.terrestrial.add_satellite(satellite)

    def place_mobiles_randomly(self, number_of_users):
        for i in range(number_of_users):
            new_mobile = device.Mobile(i, MOBILE_CACHE_CAPACITY, "LRU", MOBILE_RANGE)
            new_mobile.x = random.randint(0, TERRAIN_SIZE - 1)  # x coordinate
            new_mobile.y = random.randint(0, TERRAIN_SIZE - 1)  # y coordinate
            self.terrestrial.add_mobile(new_mobile)

    def print_cache_stats(self, message):
        print(message)
        print("Number of contents:                  {}".format(len(self.contents)))
        print("Number of self cache hits:           {}".format(self.terrestrial.self_hit))
        print("Number of d2d cache hits:            {}".format(self.terrestrial.d2d_hit))
        print("Number of base station cache hits:   {}".format(self.terrestrial.bs_hit))
        print("Number of satellite cache hits:      {}".format(self.terrestrial.sat_hit))
        print("Number of cache miss:                {}".format(self.terrestrial.miss))
        print("-------------------------------------------")

    # A random user requests file
    def request_contents_randomly(self):
        for c in self.contents:
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, c)

    # Returns the cache hit results of given algorithm and number of contents
    def num_contents_test(self, algorithm, num_contents):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.set_cache(BASE_STATION_CACHE_CAPACITY, algorithm)
        self.terrestrial.satellite.set_cache(SATELLITE_CACHE_CAPACITY, algorithm)

        for mobile in self.terrestrial.mobiles:
            mobile.set_cache(MOBILE_CACHE_CAPACITY, algorithm)

        self_hits = []
        d2d_hits = []
        bs_hits = []
        sat_hits = []
        universal = []

        for i in range(len(self.contents)):
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, self.contents[i])

            if i+1 in num_contents:
                self_hits.append(self.terrestrial.self_hit / i)
                d2d_hits.append(self.terrestrial.d2d_hit / i)
                bs_hits.append(self.terrestrial.bs_hit / i)
                sat_hits.append(self.terrestrial.sat_hit / i)
                universal.append(self.terrestrial.miss / i)

        return self_hits, d2d_hits, bs_hits, sat_hits, universal

    def compare_num_contents(self):
        num_contents = [10000, 50000, 100000, 250000, 500000]

        lru_results = self.num_contents_test("LRU", num_contents)
        mlplru_results = self.num_contents_test("MLPLRU", num_contents)
        cache_me_cache_results = self.num_contents_test("Cache-Me-Cache", num_contents)

        plotter.plot_content_comparison(lru_results, mlplru_results, cache_me_cache_results, num_contents)

    def zipf_test(self, algorithm, zipf_values):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.set_cache(BASE_STATION_CACHE_CAPACITY, algorithm)
        self.terrestrial.satellite.set_cache(SATELLITE_CACHE_CAPACITY, algorithm)

        for mobile in self.terrestrial.mobiles:
            mobile.set_cache(MOBILE_CACHE_CAPACITY, algorithm)

        self_hits = []
        d2d_hits = []
        bs_hits = []
        sat_hits = []
        universal = []

        for value in zipf_values:
            self.contents = content.generate_zipf_content(NUMBER_OF_CONTENTS, CONTENT_SIZE, value)
            for i in range(len(self.contents)):
                user = random.choice(self.terrestrial.mobiles)
                self.terrestrial.content_request(user, self.contents[i])

            self_hits.append(self.terrestrial.self_hit / len(self.contents))
            d2d_hits.append(self.terrestrial.d2d_hit / len(self.contents))
            bs_hits.append(self.terrestrial.bs_hit / len(self.contents))
            sat_hits.append(self.terrestrial.sat_hit / len(self.contents))
            universal.append(self.terrestrial.miss / len(self.contents))
            self.terrestrial.clear_caches()

        return self_hits, d2d_hits, bs_hits, sat_hits, universal

    def compare_zipf_parameter(self):
        zipf_values = [1.2, 1.3, 1.4, 1.5, 1.6]

        lru_results = self.zipf_test("LRU", zipf_values)
        mlplru_results = self.zipf_test("MLPLRU", zipf_values)
        cache_me_cache_results = self.zipf_test("Cache-Me-Cache", zipf_values)

        plotter.plot_zipf_distribution(lru_results, mlplru_results, cache_me_cache_results, zipf_values)

    def simulate_LRU(self):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.set_cache(BASE_STATION_CACHE_CAPACITY, "LRU")
        self.terrestrial.satellite.set_cache(SATELLITE_CACHE_CAPACITY, "LRU")

        for mobile in self.terrestrial.mobiles:
            mobile.set_cache(MOBILE_CACHE_CAPACITY, "LRU")

        self.request_contents_randomly()
        self.print_cache_stats("LRU")

    def simulate_MLPLRU(self):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.set_cache(BASE_STATION_CACHE_CAPACITY, "MLPLRU")
        self.terrestrial.satellite.set_cache(SATELLITE_CACHE_CAPACITY, "MLPLRU")

        for mobile in self.terrestrial.mobiles:
            mobile.set_cache(MOBILE_CACHE_CAPACITY, "MLPLRU")

        self.request_contents_randomly()
        self.print_cache_stats("MLPLRU")

    def simulate_Cache_Me_Cache(self):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.set_cache(BASE_STATION_CACHE_CAPACITY, "Cache-Me-Cache")
        self.terrestrial.satellite.set_cache(SATELLITE_CACHE_CAPACITY, "Cache-Me-Cache")

        for mobile in self.terrestrial.mobiles:
            mobile.set_cache(MOBILE_CACHE_CAPACITY, "Cache-Me-Cache")

        self.request_contents_randomly()
        self.print_cache_stats("Cache-Me-Cache")

    def simulate(self):
        self.simulate_LRU()
        self.simulate_MLPLRU()
        self.simulate_Cache_Me_Cache()
