from abc import ABC
import uuid
import datetime


class EntityBaseClass(ABC):
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(datetime.timezone.utc)
        self.updated_at = ''
        self.save()

    def save(self):
        self.updated_at = datetime.datetime.now(datetime.timezone.utc)
