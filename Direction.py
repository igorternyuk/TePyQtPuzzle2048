from enum import Enum
from collections import namedtuple
import random

Direction = namedtuple( 'Direction', ['dx', 'dy'] )

class Directions( Enum ):
    @property
    def dx( self ):
        return self.value.dx

    @property
    def dy( self ):
        return self.value.dy

    RIGHT = Direction( 1, 0 )
    UP = Direction( 0, -1 )
    LEFT = Direction( -1, 0 )
    DOWN = Direction( 0, 1 )

def get_opposite_direction( direction ):
    if( direction == Directions.LEFT ):
        return Directions.RIGHT
    elif( direction == Directions.RIGHT ):
        return Directions.LEFT
    elif( direction == Directions.UP ):
        return Directions.DOWN
    elif( direction == Directions.DOWN ):
        return Directions.UP
