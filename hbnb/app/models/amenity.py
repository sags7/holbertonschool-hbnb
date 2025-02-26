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

    """not implemented yet"""

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
