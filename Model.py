import random
from Direction import*
from matrix import*

ANIMATION_SPEED = 5

class GameState( Enum ):
    PLAYING = 1
    VICTORY = 2
    DEFEAT = 3

class Tile:
    def __init__( self, x, y, value ):
        self.x = x
        self.y = y
        self.value = value
        self.dest_x = x
        self.dest_y = y
        self.is_merged = False

    def is_sliding( self ):
        return self.x != self.dest_x or self.y != self.dest_y

    def slide( self, direction ):
        #dx = 0 if self.dest_x - self.x == 0 else (self.dest_x - self.x) / abs( self.dest_x - self.x )
        #dy = 0 if self.dest_y - self.y == 0 else (self.dest_y - self.y) / abs( self.dest_y - self.y )
        self.x += ANIMATION_SPEED * direction.dx
        self.y += ANIMATION_SPEED * direction.dy

class Model:
    def __init__( self, field_width, field_height, tile_size ):
        self.WINNING_SCORE = 2048
        self.PROBABILITY_OF_TILE_WITH_VALUE_OF_TWO = 90
        self.field_width = field_width
        self.field_height = field_height
        self.tile_size = tile_size
        self.grid = self.__create_grid_()
        self.tiles = []
        #self.tiles_to_remove = []
        #self.merged_tiles = []
        self.changed_tiles = []
        self.animation_direction = Directions.RIGHT
        self.is_animating = False
        self.score = 0
        self.max_tile_value = 2
        self.game_state = GameState.PLAYING

    def __create_grid_( self ):
        grid = []
        for row in range( self.field_height ):
            line = []
            for col in range ( self.field_width ):
                line.append( 0 )
            grid.append( line )
        return grid

    def reset( self ):
        self.grid = self.__create_grid_()
        self.tiles = []
        self.score = 0
        self.max_tile_value = 2
        self.add_tiles2()
        self.print_grid()
        self.game_state = GameState.PLAYING

    def add_tiles( self ):
        for i in range( 2 ):
            self.place_new_tile()

    def add_tiles2( self ):
        self.grid[0][0] = 2
        self.tiles.append( Tile( 0 * self.tile_size, 0 * self.tile_size, 2))
        self.grid[0][1] = 2
        self.tiles.append( Tile( 1 * self.tile_size, 0 * self.tile_size, 2))
        #self.grid[0][2] = 2
        #self.tiles.append( Tile( 2 * self.tile_size, 0 * self.tile_size, 2))
        self.grid[0][3] = 4
        self.tiles.append( Tile( 3 * self.tile_size, 0 * self.tile_size, 4))

    def place_new_tile( self ):
        if self.count_free() > 0:
            while( True ):
                rand_col = random.choice( range( self.field_width ) )
                rand_row = random.choice( range( self.field_height ) )
                if self.grid[rand_row][rand_col] == 0:
                    rand_val = 2 if random.choice( range(100) ) < self.PROBABILITY_OF_TILE_WITH_VALUE_OF_TWO else 4
                    self.grid[rand_row][rand_col] = rand_val
                    new_tile = Tile( rand_col * self.tile_size,
                     rand_row * self.tile_size, rand_val)
                    new_tile.is_merged = False
                    self.tiles.append( new_tile )
                    break
        else:
            self.game_over()

    def game_over( self ):
        self.game_state = GameState.DEFEAT

    def slide( self, direction ):
        if self.game_state != GameState.PLAYING or self.is_animating:
            return
        if direction == Directions.RIGHT:
            print("Sliding right")
            self.animation_direction = Directions.RIGHT
            self.slide_right()
        elif direction == Directions.LEFT:
            print("Sliding left")
            self.animation_direction = Directions.LEFT
            self.slide_left()
        elif direction == Directions.DOWN:
            print("Sliding down")
            self.animation_direction = Directions.DOWN
            self.slide_down()
        elif direction == Directions.UP:
            print("Sliding up")
            self.animation_direction = Directions.UP
            self.slide_up()

    def slide_down( self ):
        print("Trying to slide down")
        for j in range( self.field_width ):
            for i in range ( self.field_height - 2, -1, -1 ):
                if self.grid[i][j] > 0:
                    tile_to_slide = self.find_tile( j * self.tile_size,
                     i * self.tile_size )
                    is_merging = False
                    row = i
                    while row < self.field_height - 1:
                        if self.grid[row + 1][j] == 0:
                            self.grid[row + 1][j] = self.grid[row][j]
                            self.grid[row][j] = 0
                            row += 1
                        elif self.grid[row][j] == self.grid[row + 1][j]:
                            tile_to_merge = self.find_tile( j * self.tile_size,
                             ( row + 1 ) * self.tile_size )
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                self.grid[row + 1][j] *= 2
                                self.grid[row][j] = 0
                                print("Appending tiles for merging")
                                print("Tile to slide")
                                self.print_tile(tile_to_slide)
                                print("Tile to merge")
                                self.print_tile(tile_to_merge)
                                self.changed_tiles.append( [ tile_to_slide,
                                 tile_to_merge, False ] )
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_y = ( row + 1 ) * self.tile_size
                    else:
                        tile_to_slide.dest_y = row * self.tile_size
                    self.is_animating = True
                    self.print_grid()

    def slide_up( self ):
        print("Trying to slide up")
        for j in range( self.field_width ):
            for i in range( 1, self.field_height, 1 ):
                if self.grid[i][j] > 0:
                    tile_to_slide = self.find_tile( j * self.tile_size,
                     i * self.tile_size)
                    is_merging = False
                    row = i
                    while row > 0:
                        if self.grid[row - 1][j] == 0:
                            self.grid[row - 1][j] = self.grid[row][j]
                            self.grid[row][j] = 0
                            row -= 1
                        elif self.grid[row][j] == self.grid[row - 1][j]:
                            tile_to_merge = self.find_tile( j * self.tile_size,
                            (row - 1) * self.tile_size )
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                self.grid[row - 1][j] *= 2
                                self.grid[row][j] = 0
                                print("Appending tiles for merging")
                                print("Tile to slide")
                                self.print_tile(tile_to_slide)
                                print("Tile to merge")
                                self.changed_tiles.append([ tile_to_slide,
                                 tile_to_merge, False ])
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_y = ( row - 1 ) * self.tile_size
                    else:
                        tile_to_slide.dest_y = row * self.tile_size
                    self.is_animating = True
                    self.print_grid()

    def slide_left( self ):
        for i in range( self.field_height ):
            for j in range ( 1, self.field_width, 1 ):
                if self.grid[i][j] > 0:
                    tile_to_slide = self.find_tile( j * self.tile_size,
                     i * self.tile_size )
                    is_merging = False
                    col = j
                    while col > 0:
                        if self.grid[i][col - 1] == 0:
                            self.grid[i][col - 1] = self.grid[i][col]
                            self.grid[i][col] = 0
                            col -= 1
                        elif self.grid[i][col] == self.grid[i][col - 1]:
                            tile_to_merge = self.find_tile( ( col - 1 ) *
                            self.tile_size, i * self.tile_size)
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                self.grid[i][col - 1] *= 2
                                self.grid[i][col] = 0
                                print("Appending tiles for merging")
                                print("Tile to slide")
                                self.print_tile(tile_to_slide)
                                print("Tile to merge")
                                self.changed_tiles.append( [ tile_to_slide,
                                 tile_to_merge, False  ])
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_x = ( col - 1 ) * self.tile_size
                    else:
                        tile_to_slide.dest_x = col * self.tile_size
                    self.is_animating = True
                    self.print_grid()

    def slide_right( self ):
        for i in range( self.field_height ):
            for j in range( self.field_width - 2, -1, -1 ):
                if self.grid[i][j] > 0:
                    tile_to_slide = self.find_tile( j * self.tile_size,
                     i * self.tile_size )
                    is_merging = False
                    col = j
                    while col < self.field_width - 1:
                        if self.grid[i][col + 1] == 0:
                            self.grid[i][col + 1] = self.grid[i][col]
                            self.grid[i][col] = 0
                            col += 1
                        elif self.grid[i][col] == self.grid[i][col + 1]:
                            tile_to_merge = self.find_tile( ( col + 1 )  *
                             self.tile_size, i * self.tile_size )
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                self.grid[i][col + 1] *= 2
                                self.grid[i][col] = 0
                                print("Appending tiles for merging")
                                print("Tile to slide")
                                self.print_tile(tile_to_slide)
                                print("Tile to merge")
                                self.changed_tiles.append( [ tile_to_slide,
                                 tile_to_merge, False ] )
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_x = ( col + 1 ) * self.tile_size
                    else:
                        tile_to_slide.dest_x = col * self.tile_size
                    self.is_animating = True
                    self.print_grid()
        #self.changed_tiles = list( zip( self.tiles_to_remove, self.merged_tiles ) )

    def check_win( self ):
        if self.max_tile_value >= self.WINNING_SCORE:
            self.game_state = GameState.VICTORY

    def print_grid( self ):
        print("--------")
        for row in range( self.field_height ):
            for col in range( self.field_width ):
                print(self.grid[row][col], end = '', flush = True )
            print("")
        print("-------- tiles = ", len( self.tiles ), "--------" )

    def find_tile( self, x, y ):
        for tile in self.tiles:
            if tile.dest_x == x and tile.dest_y == y:
                return tile
        return None

    def count_free( self ):
        counter = 0
        for row in self.grid:
            #my_list = filter(lambda x: x.attribute == value, my_list)
            counter += len( [ val for val in row if val == 0 ] )
        return counter

    def check_animation( self ):
        for tile in self.tiles:
            if tile.is_sliding():
                return True
        for pair in self.changed_tiles:
            if not pair[2]:
                return True
        return False

    def tick( self ):
        if self.is_animating:
            for tile in self.tiles:
                if tile.is_sliding():
                    print("sliding")
                    tile.slide( self.animation_direction )
                #else:
                #    print("may be merge x = ", tile.x, " y = ", tile.y, "?")
                #    tile_pair = self.check_if_tile_is_in_changed_pairs( tile )
                #    if not tile_pair is None:
                #        print("merging")
                #        self.merge_tiles( tile_pair )
            for pair in self.changed_tiles:
                if ( not pair[2] ) and pair[0].x == pair[1].x and pair[0].y == pair[1].y:
                     self.merge_tiles( pair )


            self.is_animating = self.check_animation()
            if not self.is_animating:
                self.reset_merging_factor()
                self.clear_auxillary_tiles()
                self.check_win()
                self.add_tiles()
                self.print_grid()

    def print_tile( self, tile ):
        print("(", tile.x, ",", tile.y, ")->", tile.value )

    def check_if_tile_is_in_changed_pairs( self, tile ):
        print("CHECKING FUNCTION")
        print( "len( self.changed_tiles ) = ", len( self.changed_tiles ) )
        print("tiles:")
        for tile_pair in self.changed_tiles:
            self.print_tile(tile_pair[0])
            self.print_tile(tile_pair[1])
            print("******")

        for tile_pair in self.changed_tiles:
            if tile == tile_pair[0]:
                return tile_pair
        return None

    def clear_auxillary_tiles( self ):
        self.changed_tiles.clear()

    def reset_merging_factor( self ):
        for tile in self.tiles:
            tile.is_merged = False

    def merge_tiles( self, tile_pair ):
        print("Tile merging")
        tile_to_remove = tile_pair[0]
        tile_to_merge = tile_pair[1]
        print("tile_to_remove.x = ", tile_to_remove.x, " tile_to_remove.y = ", tile_to_remove.y)
        print("tile_to_merge.x = ", tile_to_merge.x, " tile_to_merge.y = ", tile_to_merge.y)
        tile_to_merge.value *= 2
        tile_to_merge.is_merged = False
        self.score += tile_to_merge.value
        if self.max_tile_value < tile_to_merge.value:
            self.max_tile_value = tile_to_merge.value
        #self.changed_tiles.remove( tile_pair )
        tile_pair[2] = True
        self.tiles.remove( tile_to_remove )
        print("Tile was removed x = ", tile_to_remove.x, " y = ", tile_to_remove.y)
