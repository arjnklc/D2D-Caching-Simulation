import random
import numpy

class Content:
    def __init__(self, size, unique_id):
        self.size = size
        self.unique_id = unique_id

    def __repr__(self):
        return str(self.unique_id)

    # Override "==" operation
    def __eq__(self, other):
        if isinstance(other, Content):
            return self.unique_id == other.unique_id

        return False


def generate_random_content(count, min_size, max_size):
    contents = []
    for i in range(count):
        size = random.randint(min_size, max_size)
        contents.append(Content(size, i))

    return contents


def generate_zipf_content(count, size, zipf_parameter):
    contents = []
    zipf_dist = numpy.random.zipf(zipf_parameter, count)
    for i in range(count):
        contents.append(Content(size, zipf_dist[i]))

    return contents
