from math import*

def create_empty_matrix( row_count, col_count ):
    matrix = []
    for i in range( row_count ):
        line = []
        for j in range( col_count ):
            line.append( 0 )
        matrix.append( line )
    return matrix

def print_matrix( matrix ):
    for line in matrix:
        print( line )

def rotate_matrix_clockwise( matrix ):
    N = len( matrix )
    for i in range( int( N / 2 ) ):
        for j in range( i, N - 1 - i ):
            tmp = matrix[N - 1 - j][i]
            matrix[N - 1 - j][i] = matrix[N - 1 - i][N - 1 - j]
            matrix[N - 1 - i][N - 1 - j] = matrix[j][N - 1 - i]
            matrix[j][N - 1 - i] = matrix[i][j]
            matrix[i][j] = tmp
    return matrix

def rotate_matrix_counterclockwise( matrix ):
    N = len( matrix )
    for i in range( int( N / 2 ) ):
        for j in range( i, N - 1 - i ):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[j][N - 1 - i]
            matrix[j][N - 1 - i] = matrix[N - 1 - j][N - 1 - i]
            matrix[N - 1 - j][N - 1 - i] = matrix[j][N - 1 - i]
            matrix[j][N - 1 - i] = tmp
    return matrix

def flip_matrix_horizontally( matrix ):
    N = len( matrix )
    for i in range( N ):
        for j in range( int( N / 2 ) ):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[i][N - 1 - j]
            matrix[i][N - 1 - j] = tmp
    return matrix

mtr = [[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,1,0]]
print_matrix( mtr )
print("-------")
r_mtr = rotate_matrix_clockwise( mtr )
print_matrix( r_mtr )
print("----Flipped-----")
def get_loctation_in_rotated_coordinate_system( location, angle ):
    location[0] -= 2
    location[1] -= 2
    nx = int(location[0] * cos(angle) + location[1] * sin( angle )) + 2
    ny = int(-location[0] * sin(angle) + location[1] * cos( angle )) + 2
    return nx, ny

print_matrix( flip_matrix_horizontally( r_mtr ) )

#nx = x*cos(A) + y*sin(A)
#nyx = -x*sin(A) + y*cos(A)
