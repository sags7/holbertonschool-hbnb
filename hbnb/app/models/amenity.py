from app.models.entity_base_class import EntityBaseClass


class Amenity(EntityBaseClass):
    def __init__(self, name):
        super().__init__()
        name = name.strip()
        if len(name) == 0:
            raise ValueError("Name cannot be empty.")
        if len(name) > 50:
            raise ValueError("Name must be 50 characters or less.")
        self.name = name

    def create(self, name):
        self.name = name
        pass

    def update(self, name):
        self.name = name
        self.save()

    """not implemented yet"""

    def read(self):
        pass

    def delete(self):
        pass
