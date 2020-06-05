import pickle
import tempfile
import os
import DNS.cache_data
class Cache:
    def __init__(self):
        self.ip_data = {}
        self.domein_name_data = {}
        self.directory_ip = os.path.join(tempfile.gettempdir(), "path.data.ip")
        self.directory_name = os.path.join(tempfile.gettempdir(), 'path.data.name')

    def create(self):
        self.ip_data = self.get_ip_data()
        self.domein_name_data = self.get_name_data()

    def get_data_by_ip(self, ip):
        data = self.ip_data.get(ip)
        return DNS.cache_data.cache_data(data['ttl'], data['data'], data['create_time'])

    def get_data_by_name(self, name):
        data = self.domein_name_data.get(name)
        return  DNS.cache_data.cache_data(data['ttl'], data['data'], data['create_time'])

    def add_data_by_ip(self, ip, data):
        self.ip_data[ip] = data.get_dict

    def add_data_by_name(self, name, data):
        self.domein_name_data[name] = data.get_dict()

    def get_ip_data(self):
        if not os.path.exists(self.directory_ip):
            return {}
        else:
            with open(self.directory_ip, 'rb') as f:
                rawData = f.read()
                if rawData:
                    return pickle.loads(rawData)

                return {}

    def get_name_data(self):
        if not os.path.exists(self.directory_name):
            return {}
        else:
            with open(self.directory_name, 'rb') as f:
                rawData = f.read()
                if rawData:
                    return pickle.loads(rawData)

                return {}

    def save(self):
        with open(self.directory_ip, 'wb') as f:
            pickle.dump(dict(self.ip_data), f)

        with open(self.directory_name, 'wb') as f:
            pickle.dump(dict(self.domein_name_data), f)

    def check_and_clean(self):
        for ip, data in self.ip_data:
            if not data.check_time_to_live():
                self.ip_data.pop(ip, None)

        for name, data in self.domein_name_data:
            if not data.check_time_to_live():
                self.ip_data.pop(name, None)

    def clear_all(self):
        self.domein_name_data.clear()
        self.ip_data.clear()
        self.save()