from abc import ABC, abstractmethod
import uuid
import datetime


class EntityBaseClass(ABC):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(datetime.timezone.utc)
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    def save(self):
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
