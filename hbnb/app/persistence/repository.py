from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Adds an object to the repository"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Returns: User: user object with obj_id"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Returns: List[objects]: all objects in the repository"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update a User object with obj_id"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Deletes a User object with obj_id"""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Returns: User: user object with attr_name equal to attr_value"""
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name) == attr_value),
            None)
