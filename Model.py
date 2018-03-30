import random
from Direction import*

class Model:
    def __init__( self, field_width, field_height, tile_size ):
        self.field_width = field_width
        self.field_height = field_height
        self.tile_size = tile_size
        self.values = [ 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048 ]
        self.grid = self.__create_grid_()

    def __create_grid_( self ):
        grid = []
        for row in range( self.field_height ):
            line = []
            for col in range ( self.field_width ):
                rand_val = self.values[ random.choice( range( 11 ) ) ]
                line.append( Tile( col * self.tile_size, row * self.tile_size,
                 rand_val ) )
            grid.append( line )
        return grid

    def reset( self ):
        pass

    def slide( self ):
        pass

    def tick( self ):
        pass


class Tile:
    def __init__( self, x, y, value ):
        self.x = x
        self.y = y
        self.value = value
