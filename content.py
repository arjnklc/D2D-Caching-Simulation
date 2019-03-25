import random


class Content:
    def __init__(self, size, unique_id):
        self.size = size
        self.unique_id = unique_id



def generate_random_content(count, min_size, max_size):
    contents = []
    for i in range(count):
        size = random.randint(min_size, max_size)
        contents.append(Content(size, i))

    return contents


