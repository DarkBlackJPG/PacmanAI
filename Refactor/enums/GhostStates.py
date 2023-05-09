import enum


class GhostStates(enum.IntEnum):
    """Ghost states"""
    SCATTER = 0
    CHASE = 1
    FRIGHTENED = 2
    EATEN = 3
    IN_HOUSE = 4
