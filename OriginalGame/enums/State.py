from enum import Enum


class State(Enum):
    IN_HOUSE = 0
    SCATTER = 1
    CHASE = 2
    FRIGHTENED = 3
    EATEN = 4
