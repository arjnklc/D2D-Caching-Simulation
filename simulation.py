import terrain
import device
import content
import random

from parameters import *


class Simulator:



    def __init__(self):
        self.hit_count = 0
        self.miss_count = 0

        self.terrestrial = terrain.Terrain(TERRAIN_SIZE)

        base_station = device.BaseStation(BASE_STATION_CACHE_CAPACITY, "LRU", BASE_STATION_RANGE)
        base_station.x = int(TERRAIN_SIZE / 2)
        base_station.y = int(TERRAIN_SIZE / 2)  # Located in center of terrain
        self.terrestrial.add_base_station(base_station)

        satellite = device.Satellite(SATELLITE_CACHE_CAPACITY, "LRU", SATELLITE_DISTANCE)
        self.terrestrial.add_satellite(satellite)

        for _ in range(NUMBER_OF_USERS):
            new_mobile = device.Mobile(MOBILE_CACHE_CAPACITY, "LRU", MOBILE_RANGE)
            new_mobile.x = random.randint(0, TERRAIN_SIZE)  # x coordinate
            new_mobile.y = random.randint(0, TERRAIN_SIZE)  # y coordinate
            self.terrestrial.add_mobile(new_mobile)


        self.contents = content.generate_random_content(NUMBER_OF_CONTENTS, MIN_CONTENT_SIZE, MAX_CONTENT_SIZE)



    def simulate_LRU(self):
        self.hit_count = 0
        self.miss_count = 0

        self.terrestrial.base_station.algorithm = "LRU"
        self.terrestrial.satellite.algorithm = "LRU"

        for mobile in self.terrestrial.mobiles:
            mobile.algorithm = "LRU"


        for c in self.contents:
            user = random.choice(self.terrestrial.mobiles)
            self.terrestrial.content_request(user, c)


    def simulate(self):
        self.simulate_LRU()
        # self.simulate_MLPLRU()
        # self.simulate_Cache_Me_Cache()
