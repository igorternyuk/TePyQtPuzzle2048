class Tile:
    def __init__( self, x, y, value ):
        self.x = x
        self.y = y
        self.value = value
        self.dest_x = x
        self.dest_y = y
        self.ANIMATION_SPEED = 10
        self.is_merged = False

    def is_sliding( self ):
        return self.x != self.dest_x or self.y != self.dest_y

    def slide( self, direction ):
        self.x += self.ANIMATION_SPEED * direction.dx
        self.y += self.ANIMATION_SPEED * direction.dy

    def __str__( self ):
        return "(" + str(self.x) + ", " + str(self.y) + ") -> "
        + str( self.value )
