import random
import math
from parameters import *


class Cell:
    def __init__(self):
        self.devices = []


class Terrain:

    def __init__(self, size):
        self.size = size
        self.mobiles = []
        self.cells = [[Cell() for _ in range(size)] for _ in range(size)]

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
            if self.distance_between(m, user) <= MOBILE_RANGE and m.cache.contains(content):
                return True

        return False

    def content_request(self, user, content):
        if user.cache.contains(content):
            print("self hit cache!")
        elif self.contains_in_neighbours(user, content):
            print("d2d cache hit")
        elif self.base_station.cache.contains(content):
            print("get from base station cache")
        elif self.satellite.cache.contains(content):
            print("get from satellite cache")
        else:
            print("get from universal source")


