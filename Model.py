import random, copy
from Direction import*
from Tile import*

class GameState( Enum ):
    PLAYING = 1
    VICTORY = 2
    DEFEAT = 3

class Model:
    def __init__( self, field_width, field_height, tile_size ):
        self.WINNING_SCORES= { 3:1024, 4:2048, 5:4096 }
        self.TWO_PROBABILITY = 90
        self.field_width = field_width
        self.field_height = field_height
        self.tiles = []
        self.score = 0
        self.max_tile_value = 2
        self.game_state = GameState.PLAYING
        self.__winnig_score = self.WINNING_SCORES[ field_width ]
        self.__tile_size = tile_size
        self.__number_of_new_tiles = 2 if field_width == 4 or field_width == 5 else 1
        self.__grid = self.__create_grid_()
        self.__old_greed = []
        self.__tiles_moved = False
        self.__merging_tiles = []
        self.__animation_direction = Directions.RIGHT
        self.__is_animating = False

    def __create_grid_( self ):
        grid = []
        for row in range( self.field_height ):
            line = []
            for col in range ( self.field_width ):
                line.append( 0 )
            grid.append( line )
        return grid

    def reset( self ):
        self.__grid = self.__create_grid_()
        self.tiles = []
        self.score = 0
        self.__add_tiles_()
        self.__update_max_tile_value_()
        self.print_grid()
        self.game_state = GameState.PLAYING

    def __add_tiles_( self ):
        for i in range( self.__number_of_new_tiles ):
            self.__place_new_tile_()

    def __place_new_tile_( self ):
        if self.__count_free_spots_() > 0:
            while( True ):
                rand_col = random.choice( range( self.field_width ) )
                rand_row = random.choice( range( self.field_height ) )
                if self.__grid[rand_row][rand_col] == 0:
                    rand_val = 2
                    if random.choice( range(100) ) > self.TWO_PROBABILITY:
                        rand_val = 4
                    self.__grid[rand_row][rand_col] = rand_val
                    new_tile = Tile( rand_col * self.__tile_size,
                     rand_row * self.__tile_size, rand_val)
                    new_tile.is_merged = False
                    self.tiles.append( new_tile )
                    break
        else:
            self.__game_over_()

    def __game_over_( self ):
        self.game_state = GameState.DEFEAT

    def slide( self, direction ):
        if self.game_state != GameState.PLAYING or self.__is_animating:
            return
        self.__old_greed = copy.deepcopy( self.__grid )
        if direction == Directions.RIGHT:
            self.__animation_direction = Directions.RIGHT
            self.__slide_right_()
        elif direction == Directions.LEFT:
            self.__animation_direction = Directions.LEFT
            self.__slide_left_()
        elif direction == Directions.DOWN:
            self.__animation_direction = Directions.DOWN
            self.__slide_down_()
        elif direction == Directions.UP:
            self.__animation_direction = Directions.UP
            self.__slide_up_()

    def __slide_down_( self ):
        for j in range( self.field_width ):
            for i in range ( self.field_height - 2, -1, -1 ):
                if self.__grid[i][j] > 0:
                    tile_to_slide = self.__find_tile_by_coords_( j * self.__tile_size,
                     i * self.__tile_size )
                    row = i
                    is_merging = False
                    while row < self.field_height - 1:
                        if self.__grid[row + 1][j] == 0:
                            self.__grid[row + 1][j] = self.__grid[row][j]
                            self.__grid[row][j] = 0
                            row += 1
                        elif self.__grid[row][j] == self.__grid[row + 1][j]:
                            tile_to_merge = self.__find_tile_by_coords_(
                             j * self.__tile_size, ( row + 1 ) * self.__tile_size )
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                tile_to_slide.is_merged = True
                                self.__grid[row + 1][j] *= 2
                                self.__grid[row][j] = 0
                                print( str( tile_to_slide ) )
                                print( str( tile_to_merge ) )
                                self.__merging_tiles.append( [ tile_to_slide,
                                 tile_to_merge, False ] )
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_y = ( row + 1 ) * self.__tile_size
                    else:
                        tile_to_slide.dest_y = row * self.__tile_size
                    self.__is_animating = True
                    self.print_grid()

    def __slide_up_( self ):
        for j in range( self.field_width ):
            for i in range( 1, self.field_height, 1 ):
                if self.__grid[i][j] > 0:
                    tile_to_slide = self.__find_tile_by_coords_(
                     j * self.__tile_size, i * self.__tile_size)
                    row = i
                    is_merging = False
                    while row > 0:
                        if self.__grid[row - 1][j] == 0:
                            self.__grid[row - 1][j] = self.__grid[row][j]
                            self.__grid[row][j] = 0
                            row -= 1
                        elif self.__grid[row][j] == self.__grid[row - 1][j]:
                            tile_to_merge = self.__find_tile_by_coords_(
                             j * self.__tile_size, (row - 1) * self.__tile_size )
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                tile_to_slide.is_merged = True
                                self.__grid[row - 1][j] *= 2
                                self.__grid[row][j] = 0
                                print( str( tile_to_slide ) )
                                print( str( tile_to_merge ) )
                                self.__merging_tiles.append([ tile_to_slide,
                                 tile_to_merge, False ])
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_y = ( row - 1 ) * self.__tile_size
                    else:
                        tile_to_slide.dest_y = row * self.__tile_size
                    self.__is_animating = True
                    self.print_grid()

    def __slide_left_( self ):
        for i in range( self.field_height ):
            for j in range ( 1, self.field_width, 1 ):
                if self.__grid[i][j] > 0:
                    tile_to_slide = self.__find_tile_by_coords_(
                     j * self.__tile_size, i * self.__tile_size )
                    col = j
                    is_merging = False
                    while col > 0:
                        if self.__grid[i][col - 1] == 0:
                            self.__grid[i][col - 1] = self.__grid[i][col]
                            self.__grid[i][col] = 0
                            col -= 1
                        elif self.__grid[i][col] == self.__grid[i][col - 1]:
                            tile_to_merge = self.__find_tile_by_coords_(
                             ( col - 1 ) * self.__tile_size, i * self.__tile_size)
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                tile_to_slide.is_merged = True
                                self.__grid[i][col - 1] *= 2
                                self.__grid[i][col] = 0
                                print( str( tile_to_slide ) )
                                print( str( tile_to_merge ) )
                                self.__merging_tiles.append( [ tile_to_slide,
                                 tile_to_merge, False  ])
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_x = ( col - 1 ) * self.__tile_size
                    else:
                        tile_to_slide.dest_x = col * self.__tile_size
                    self.__is_animating = True
                    self.print_grid()

    def __slide_right_( self ):
        for i in range( self.field_height ):
            for j in range( self.field_width - 2, -1, -1 ):
                if self.__grid[i][j] > 0:
                    tile_to_slide = self.__find_tile_by_coords_(
                     j * self.__tile_size, i * self.__tile_size )
                    col = j
                    is_merging = False
                    while col < self.field_width - 1:
                        if self.__grid[i][col + 1] == 0:
                            self.__grid[i][col + 1] = self.__grid[i][col]
                            self.__grid[i][col] = 0
                            col += 1
                        elif self.__grid[i][col] == self.__grid[i][col + 1]:
                            tile_to_merge = self.__find_tile_by_coords_(
                             ( col + 1 ) * self.__tile_size, i * self.__tile_size )
                            if not tile_to_merge.is_merged:
                                tile_to_merge.is_merged = True
                                tile_to_slide.is_merged = True
                                self.__grid[i][col + 1] *= 2
                                self.__grid[i][col] = 0
                                print( str( tile_to_slide ) )
                                print( str( tile_to_merge ) )
                                self.__merging_tiles.append( [ tile_to_slide,
                                 tile_to_merge, False ] )
                                is_merging = True
                            break
                        else:
                            break
                    if is_merging:
                        tile_to_slide.dest_x = ( col + 1 ) * self.__tile_size
                    else:
                        tile_to_slide.dest_x = col * self.__tile_size
                    self.__is_animating = True
                    self.print_grid()

    def __check_if_something_moved_( self ):
        for i in range( self.field_height ):
            for j in range( self.field_width ):
                if self.__grid[i][j] != self.__old_greed[i][j]:
                    return True
        return False

    def __check_win_( self ):
        if self.max_tile_value >= self.__winnig_score:
            self.game_state = GameState.VICTORY

    def print_grid( self ):
        print("--------")
        for row in range( self.field_height ):
            for col in range( self.field_width ):
                print(self.__grid[row][col], end = '', flush = True )
            print("")
        print("-------- tiles = ", len( self.tiles ), "--------" )

    def __find_tile_by_coords_( self, x, y ):
        for tile in self.tiles:
            if tile.dest_x == x and tile.dest_y == y:
                return tile
        return None

    def __count_free_spots_( self ):
        counter = 0
        for row in self.__grid:
            #my_list = filter(lambda x: x.attribute == value, my_list)
            counter += len( [ val for val in row if val == 0 ] )
        return counter

    def __check_animation_( self ):
        for tile in self.tiles:
            if tile.is_sliding():
                return True
        for pair in self.__merging_tiles:
            if not pair[2]:
                return True
        return False

    def tick( self ):
        if self.__is_animating:
            for tile in self.tiles:
                if tile.is_sliding():
                    tile.slide( self.__animation_direction )
            for pair in self.__merging_tiles:
                if ( not pair[2] ) and pair[0].x == pair[1].x and pair[0].y == pair[1].y:
                     self.__merge_tiles_( pair )
            self.__is_animating = self.__check_animation_()
            if not self.__is_animating:
                self.__merging_tiles.clear()
                #self.__synchronize_tiles_with_grid_()
                self.__check_win_()
                self.__reset_merging_factor_()
                if self.__check_if_something_moved_():
                    self.__add_tiles_()
                self.print_grid()

    def __synchronize_tiles_with_grid_ ( self ):
        if self.__is_animating:
            return
        for i in range( self.field_height ):
            for j in range( self.field_width ):
                if self.__grid[i][j] > 0:
                    tile = self.__find_tile_by_coords_(
                     j * self.__tile_size, i * self.__tile_size)
                    tile.value = self.__grid[i][j]

    def __reset_merging_factor_( self ):
        for tile in self.tiles:
            tile.is_merged = False

    def __merge_tiles_( self, tile_pair ):
        tile_to_remove = tile_pair[0]
        tile_to_merge = tile_pair[1]
        tile_to_merge.value *= 2
        self.score += tile_to_merge.value
        if self.max_tile_value < tile_to_merge.value:
            self.max_tile_value = tile_to_merge.value
        tile_pair[2] = True
        self.tiles.remove( tile_to_remove )

    def __update_max_tile_value_( self ):
        for tile in self.tiles:
            if tile.value > self.max_tile_value:
                self.max_tile_value = tile.value
