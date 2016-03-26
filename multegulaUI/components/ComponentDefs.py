from enum import Enum

class Orientation(Enum):
    DIR_NORTH = 0;
    DIR_SOUTH = 1;
    DIR_EAST = 2;
    DIR_WEST = 3;

class Direction(Enum):
    DIR_STOP = 0;
    DIR_LEFT = 1;
    DIR_RIGHT = 2;

class PowerUps(Enum):
    PWR_NONE = 0;
