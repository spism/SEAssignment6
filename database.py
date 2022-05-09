
class Database:

    def _init_(self, name):
        self.list = dict()
        self.name = name

    def add_object(self, object):
        if object.get_id not in self.list.keys():
            self.list[object.get_id()] = object

    def remove_object(self, object):
        self.list[object.get_id()] = None

    def get_object(self, id):
        return self.list[id]

    def update_object(self, id, object):
        self.list[id] = object
