import random
import math
from enum import Enum

from parameters import *



class Cell:
    def __init__(self):
        self.devices = []


class Terrain:

    def __init__(self, size):
        self.size = size
        self.mobiles = []
        self.self_hit, self.d2d_hit, self.bs_hit, self.sat_hit, self.miss = 0, 0, 0, 0, 0
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]

    def clear_caches(self):
        self.self_hit, self.d2d_hit, self.bs_hit, self.sat_hit, self.miss = 0, 0, 0, 0, 0
        self.satellite.cache.clear()
        self.base_station.cache.clear()
        for m in self.mobiles:
            m.cache.clear()

    def locate_device(self, device, x, y):
        self.cells[x][y].devices.append(device)

    def add_satellite(self, satellite):
        self.satellite = satellite

    def add_base_station(self, base_station):
        self.base_station = base_station
        self.locate_device(self.base_station, self.base_station.x, self.base_station.y)

    def add_mobile(self, mobile):
        self.mobiles.append(mobile)
        self.locate_device(mobile, mobile.x, mobile.y)

    # Euclidean distance between two devices
    def distance_between(self, device1, device2):
        return math.sqrt((device1.x - device2.x) ** 2 + (device1.y - device2.y) ** 2)

    # Return true if the specified content contains in one of the neighbours' cache
    def contains_in_neighbours(self, user, content):
        for m in self.mobiles:
            if self.distance_between(m, user) <= MOBILE_RANGE:
                if m.cache.contains(content):
                    m.cache.new_content(content)
                    return True

        return False



    def content_request(self, user, content):
        if user.cache.contains(content):
            self.self_hit += 1
        elif self.contains_in_neighbours(user, content):
            self.d2d_hit += 1
        elif self.base_station.cache.contains(content):
            self.base_station.cache.new_content(content)
            self.bs_hit += 1
        elif self.satellite.cache.contains(content):
            self.satellite.cache.new_content(content)
            self.sat_hit += 1
        else:
            self.base_station.cache.new_content(content)
            self.satellite.cache.new_content(content)
            self.miss += 1

        # Cache the new content
        user.cache.new_content(content)
