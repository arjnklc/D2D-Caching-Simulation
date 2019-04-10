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

    def print_cache_stats(self):
        print("Number of contents:                  {}".format(len(self.contents)))
        print("Number of self cache hits:           {}".format(self.terrestrial.self_hit))
        print("Number of d2d cache hits:            {}".format(self.terrestrial.d2d_hit))
        print("Number of base station cache hits:   {}".format(self.terrestrial.bs_hit))
        print("Number of satellite cache hits:      {}".format(self.terrestrial.sat_hit))
        print("Number of cache miss:                {}".format(self.terrestrial.miss))

    # A random user requests file
    def request_contents_randomly(self):
        for c in self.contents:
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, c)


    def test_for_num_contents(self):
        self_hits = []
        d2d_hits = []
        bs_hits = []
        sat_hits = []
        universal = []
        contents_intervals = [50, 500, 5000, 50000, 500000]

        for i in range(len(self.contents)):
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, self.contents[i])

            if i+1 in contents_intervals:
                self_hits.append(self.terrestrial.self_hit / i)
                d2d_hits.append(self.terrestrial.d2d_hit / i)
                bs_hits.append(self.terrestrial.bs_hit / i)
                sat_hits.append(self.terrestrial.sat_hit / i)
                universal.append(self.terrestrial.miss / i)

        plotter.plot_content_comparison(self_hits, d2d_hits, bs_hits, sat_hits, universal, contents_intervals)


    def test_for_zipf_parameter(self):
        self_hits = []
        d2d_hits = []
        bs_hits = []
        sat_hits = []
        universal = []
        zipf_values = [1.2, 1.3, 1.4, 1.5, 1.6]
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

        plotter.plot_zipf_distribution(self_hits, d2d_hits, bs_hits, sat_hits, universal, zipf_values)



    def simulate_LRU(self):
        self.terrestrial.clear_caches()
        self.terrestrial.base_station.algorithm = "LRU"
        self.terrestrial.satellite.algorithm = "LRU"

        for mobile in self.terrestrial.mobiles:
            mobile.algorithm = "LRU"

        self.request_contents_randomly()
        self.print_cache_stats()


    def simulate_MLPLRU(self):
        pass

    def simulate(self):
        self.simulate_LRU()
        # self.simulate_MLPLRU()
        # self.simulate_Cache_Me_Cache()
