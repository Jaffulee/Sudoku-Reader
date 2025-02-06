import numpy as np

class Sudoku:
    possible_numbers_set = {1,2,3,4,5,6,7,8,9}

    def __init__(self,sudoku_str=None,sudoku_array=None):
        if sudoku_str is not None:
            self.sudoku_str = sudoku_str
            self.sudoku_array = self.get_rows()
        elif sudoku_array is not None:
            self.sudoku_array = np.array(sudoku_array,dtype=int)
            self.sudoku_str = self.get_sudoku_str()
        else:
            raise ValueError('Enter a string representation or array representation of the Sudoku puzzle')
        self.rows = self.sudoku_array
        self.columns = self.get_columns()
        self.boxes = self.get_boxes()

    def get_rows(self):
        '''
        Returns a 9x9 numpy array of adjacent numbers in rows from left to right, top to bottom.
        '''
        pos = 0
        sudoku_array = np.zeros((9, 9), dtype=int)
        for item in self.sudoku_str:
            row_number = pos//9
            column_number = pos%9
            sudoku_array[row_number][column_number]=int(item)
            pos += 1
        return sudoku_array

    def get_columns(self):
        '''
        Returns a 9x9 numpy array of adjacent numbers in columns from left to right, top to bottom.
        '''
        return self.sudoku_array.transpose()

    def get_boxes(self):
        '''
        Returns a 9x9 numpy array of adjacent numbers in boxes from left to right, top to bottom.
        '''
        pos = 0
        sudoku_array = np.zeros((9, 9), dtype=int)
        for item in self.sudoku_str:
            row_number = (pos//3)%3 + 3*(pos//(9*3))
            column_number = pos%3 + (3*(pos//9))%9
            sudoku_array[row_number][column_number]=int(item)
            pos += 1
        return sudoku_array

    def row_pos(self,i,j):
        '''
        Returns the (i, j)th index in Sudoku.rows corresponding to the (i, j)th index in Sudoku.sudoku_array
        '''
        return i,j

    def column_pos(self,i,j):
        '''
        Returns the (i, j)th index in Sudoku.columns corresponding to the (i, j)th index in Sudoku.sudoku_array
        '''
        return j,i

    def box_pos(self,i,j):
        '''
        Returns the (i, j)th index in Sudoku.boxes corresponding to the (i, j)th index in Sudoku.sudoku_array
        '''
        pos = j+i//9
        return (pos//3)%3 + 3*(pos//(9*3)) , pos%3 + (3*(pos//9))%9

    def row_adjacency(self,i,j,excludeself=True):
        '''
        Returns the set of values adjacent to the (i, j)th entry of Sudoku.sudoku_array in Sudoku.rows, i.e. in the same row.
        '''
        row_i,row_j = self.row_pos(i,j)
        s = set()
        adj = self.rows[row_i].tolist()
        for pos,item in enumerate(adj):
            if item==0 or (pos==row_j and excludeself):
                continue
            s.add(item)
        return s

    def column_adjacency(self,i,j,excludeself=True):
        '''
        Returns the set of values adjacent to the (i, j)th entry of Sudoku.sudoku_array in Sudoku.columns, i.e. in the same column
        '''
        column_i,column_j = self.column_pos(i,j)
        s = set()
        adj = self.columns[column_i].tolist()
        for pos,item in enumerate(adj):
            if item==0 or (pos==column_j and excludeself):
                continue
            s.add(item)
        return s

    def box_adjacency(self,i,j,excludeself=True):
        '''
        Returns the set of values adjacent to the (i, j)th entry of Sudoku.sudoku_array in Sudoku.boxes, i.e. in the same box
        '''
        box_i,box_j = self.box_pos(i,j)
        s = set()
        adj = self.boxes[box_i].tolist()
        for pos,item in enumerate(adj):
            if item==0 or (pos==box_j and excludeself):
                continue
            s.add(item)
        return s

    def adjacency(self,i,j,excludeself=True):
        '''
        Returns the set of values adjacent to the (i,j)th entry of Sudoku.sudoku_array
        '''
        return self.row_adjacency(i,j,excludeself).union(self.column_adjacency(i,j,excludeself),self.box_adjacency(i,j,excludeself))

    def check_available_numbers_by_counting(self,i,j,excludeself=True):
        '''
        Returns the set of available numbers in the (i,j)th entry of Sudoku.sudoku_array, if that entry were 0 by default
        '''
        return self.possible_numbers_set.difference(self.adjacency(i,j,excludeself))

    def get_sudoku_str(self):
        '''
        Returns the Sudoku string from a 9x9 numpy array
        '''
        sudoku_str = ''
        for row in self.sudoku_array:
            for pos in range(9):
                sudoku_str+= str(row[pos])
        return sudoku_str

    def get_next_step_by_counting_DEV(self,stopatfirst=True,checkfilled=True):
        '''
        Returns a zip of (i,j,value) for each (i,j)th entry of Sudoku.sudoku_array which has a unique value by counting.
        '''
        i_array = []
        j_array = []
        value_array = []
        stop=False
        for i in range(9):
            for j in range(9):
                if self.sudoku_array[i][j]!=0 and checkfilled: # Skip non-zero values unless checkfilled = False, used for sanity checking
                    continue
                available = self.check_available_numbers_by_counting(i,j)
                length_available = len(available)
                if length_available==1:
                    i_array.append(i)
                    j_array.append(j)
                    value_array.append(available.pop())
                    if stopatfirst:
                        stop = True
                        break
                elif length_available==0: #Come back to this error checking
                    mistake=True
                    print('found mistake')
            if stop:
                break
        return zip(i_array,j_array,value_array)

    def is_filled(self):
        '''
        Returns True if all values are non-zero.
        '''
        for i in range(9):
            for j in range(9):
                not_filled = self.sudoku_array[i][j]==0
                if not_filled:
                    break
            if not_filled:
                break
        return not not_filled

    def solve_by_counting(self,overwrite=False,asarray=True):
        self.steps = []
        if asarray:
            self.steps.append(self.sudoku_array)
        else: self.steps.append(self.sudoku_str)
        # need while not filled AND while get next steps finds any steps, append each step (or overwrite self.sudoku stuff)
        return self.steps




    def __str__(self):
        return self.sudoku_array.__str__()


if __name__=='__main__':
    sudoku = Sudoku(
        sudoku_str="070000043040009610800634900094052000358460020000800530080070091902100005007040802"
        )

    print(sudoku)
    print(sudoku.rows)
    print(sudoku.columns)
    print(sudoku.boxes)
    print()

    i=0
    j=7

    print(sudoku.sudoku_array[i][j])
    print(sudoku.column_pos(i,j))
    print(sudoku.box_pos(i,j))
    print()
    print(sudoku.row_adjacency(i,j))
    print(sudoku.column_adjacency(i,j))
    print(sudoku.box_adjacency(i,j))
    print(sudoku.adjacency(i,j))
    print(sudoku.check_available_numbers_by_counting(i,j))
    print(list(sudoku.get_next_step_by_counting_DEV(
        stopatfirst=False,checkfilled=False
        )))
    print(sudoku.is_filled())
    print(sudoku.get_sudoku_str())


    sudoku_from_array = Sudoku(
        sudoku_array=sudoku.sudoku_array
    )
    print(sudoku_from_array.box_adjacency(i,j))
    print()

    completed_sudoku = Sudoku('679518243543729618821634957794352186358461729216897534485276391962183475137945862')
    print(completed_sudoku.is_filled())
