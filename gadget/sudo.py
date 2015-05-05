# -*- coding: utf-8 -*-
import os

class deSudoku:
    def __init__(self, sudoku):
        print("init...")
        self.sudoku = sudoku 
        self.full = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def nuInRow(self, row): 
        '''find number on row'''
        return [i for i in self.full if i in self.sudoku[row]]
    def emptyNuInRow(self, row): 
        '''find empty site on row'''
        return [i for i in self.full if not i in self.sudoku[row]]
        #set= [] 
        #for i in range(0, 9):
        #    if self.full[self.sudoku[row][i] - 1] == self.sudoku[row][i]:
        #        set.append(self.sudoku[row][i])
        #print(set)

    def nuInRow(self, column): 
        '''find number on column'''
        return [i for i in self.full if i in self.sudoku[i-1][column]]
    def emptyNuInColumn(self, column): 
        print("find empty site on column")
        return [i for i in self.full if not i in self.sudoku[i-1][column]]

    def emptyNuInSquare(self, square): 
        print("find empty site on square")

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
    de.printSudoku()
