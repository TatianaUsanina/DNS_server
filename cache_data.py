import time

class cache_data:

    def __init__(self, ttl, data, create_time):
        self.ttl = ttl
        self.data = data
        self.create_time = create_time

    def check_time_to_live(self):
        time_lived = time.time() - self.create_time
        return time_lived < self.ttl

    def get_dict(self):
        return {'ttl' : self.ttl,
                'data' : self.data,
                'create_time' : self.create_time}