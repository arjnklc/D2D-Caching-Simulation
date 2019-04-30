import math


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

    def can_communicate(self, device, other_device):
        return self.distance_between(device, other_device) < max(device.range, other_device.range)

    # Return true if the specified content contains in one of the neighbours' cache
    def contains_in_neighbours(self, user, content):
        for m in self.mobiles:
            if self.can_communicate(user, m):
                if m.cache.contains(content):
                    m.cache.new_content(content)
                    return True

        return False

    def contains_in_base_station(self, user, content):
        if self.can_communicate(user, self.base_station):
            if self.base_station.cache.contains(content):
                self.base_station.cache.new_content(content)
                return True

        return False

    def contains_in_satellite(self, content):
        if self.satellite.cache.contains(content):
            self.satellite.cache.new_content(content)
            return True

        return False

    def content_request(self, user, content):
        if user.cache.contains(content):
            self.self_hit += 1

        elif self.contains_in_neighbours(user, content):
            self.d2d_hit += 1

        elif self.contains_in_base_station(user, content):
            self.bs_hit += 1

        elif self.contains_in_satellite(content):
            self.sat_hit += 1

        else:
            if self.can_communicate(user, self.base_station):
                self.base_station.cache.new_content(content)
            else:
                self.satellite.cache.new_content(content)

            self.miss += 1

        # Cache the new content
        user.cache.new_content(content)
