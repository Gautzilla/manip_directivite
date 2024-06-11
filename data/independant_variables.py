from enum import Enum

class Distance(Enum):
    CLOSE: int = 1
    FAR: int = 4

class Source(Enum):
    HUMAN = 'Human'
    LOUDSPEAKER = 'Loudspeaker'

class Angle(Enum):
    FRONT = 'Front'
    SIDE = 'Side'