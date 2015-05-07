# -*- coding: utf-8 -*-
import os

class deSudoku:
    def __init__(self, sudoku):
        print("init...")
        self.sudoku = sudoku 
        self.full = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def nuInRow(self, row): 
        '''find mark site on row'''
        return [i for i in self.full if i in self.sudoku[row]]
    def emptyNuInRow(self, row): 
        '''find empty site on row'''
        return [i for i in self.full if not i in self.sudoku[row]]
        #set= [] 
        #for i in range(0, 9):
        #    if self.full[self.sudoku[row][i] - 1] == self.sudoku[row][i]:
        #        set.append(self.sudoku[row][i])
        #print(set)

    def nuInColumn(self, column): 
        '''find mark site on column'''
        set = [] 
        for i in range(0, 9):
            if self.full[self.sudoku[i][column] - 1] == self.sudoku[i][column]:
                set.append(self.sudoku[i][column])
        return set
         
    def emptyNuInColumn(self, column): 
        '''find empty site on column'''
        set = self.nuInColumn(column)
        return [i for i in self.full if not i in set]

    def getNuInSquare(self, square): 
        '''get all number on square
                     1|2|3
          square =   4|5|6
                     7|8|9 
        '''
        set = []
        set += self.sudoku[((square-1)/3)*3][((square%3-1)*3) : (3+(square%3-1)*3)]
        set += self.sudoku[((square-1)/3)*3+1][((square%3-1)*3) : (3+(square%3-1)*3)]
        set += self.sudoku[((square-1)/3)*3+2][((square%3-1)*3) : (3+(square%3-1)*3)]
        return set
    def emptyNuInSquare(self, square): 
        '''find empty site on square'''
        return [i for i in self.full if not i in self.getNuInSquare(square)]
    def nuInSquare(self, square): 
        '''find mark site on square'''
        return [i for i in self.full if i in self.getNuInSquare(square)]

    def printSudoku(self):
        print('###########################')
        for i in range(0, 9):
            print(self.sudoku[i])
        print('###########################\n')

if __name__ == '__main__':
    test = [
            [0, 3, 6, 0, 0, 0, 0, 0, 2],
            [0, 0, 5, 0, 0, 9, 0, 0, 0],
            [9, 0, 2, 4, 0, 0, 0, 0, 8],
            [0, 0, 0, 0, 3, 0, 0, 7, 4],
            [0, 0, 0, 0, 5, 0, 0, 0, 0],
            [3, 9, 0, 0, 8, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 1, 4, 0, 7],
            [0, 0, 0, 7, 0, 0, 1, 0, 0],
            [2, 0, 0, 0, 0, 0, 3, 8, 0]
            ]
    de = deSudoku(test)
    print de.emptyNuInRow(0)
    print de.nuInRow(0)
    print de.nuInColumn(0)
    print de.emptyNuInColumn(0)
    print de.getNuInSquare(5)
    print de.nuInSquare(5)
    print de.emptyNuInSquare(5)
    de.printSudoku()
