from enum import Enum


class Entity(Enum):
    """Enum to hold all the entities that will be queried against."""

    SANDBOX = "Sandboxes"
    CUBE = "Cubes"
    DIMENSION = "Dimensions"
