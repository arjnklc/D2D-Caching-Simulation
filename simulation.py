import terrain
import device
import content
import random

from parameters import *


class Simulator:

    def simulate_LRU(self):

        terrestrial = terrain.Terrain(TERRAIN_SIZE)

        base_station = device.BaseStation(BASE_STATION_CACHE_CAPACITY, "LRU", BASE_STATION_RANGE)
        base_station.x = int(TERRAIN_SIZE / 2)
        base_station.y = int(TERRAIN_SIZE / 2)  # Located in center of terrain
        terrestrial.add_base_station(base_station)

        satellite = device.Satellite(SATELLITE_CACHE_CAPACITY, "LRU", SATELLITE_DISTANCE)
        terrestrial.add_satellite(satellite)

        for _ in range(NUMBER_OF_USERS):
            new_mobile = device.Mobile(MOBILE_CACHE_CAPACITY, "LRU", MOBILE_RANGE)
            new_mobile.x = random.randint(0, TERRAIN_SIZE)  # x coordinate
            new_mobile.y = random.randint(0, TERRAIN_SIZE)  # y coordinate
            terrestrial.add_mobile(new_mobile)



        contents = content.generate_random_content(NUMBER_OF_CONTENTS, MIN_CONTENT_SIZE, MAX_CONTENT_SIZE)

        for c in contents:
            user = random.choice(terrestrial.mobiles)
            terrestrial.content_request(user, c)


    def simulate(self):
        self.simulate_LRU()
        # self.simulate_MLPLRU()
        # self.simulate_Cache_Me_Cache()
