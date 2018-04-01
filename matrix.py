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
