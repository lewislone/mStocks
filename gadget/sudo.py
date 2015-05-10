# -*- coding: utf-8 -*-
import os

class deSudoku:
    def __init__(self, sudoku):
        print("init...")
        self.sudoku = sudoku 
        self.full = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def printSudoku(self):
        print('###########################')
        for i in range(0, 9):
            print(self.sudoku[i])
        print('###########################\n')

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
        set += self.sudoku[((square-1)/3)*3][((square%3)*2) : (3+(square%3)*2)]
        set += self.sudoku[((square-1)/3)*3+1][((square%3)*2) : (3+(square%3)*2)]
        set += self.sudoku[((square-1)/3)*3+2][((square%3)*2) : (3+(square%3)*2)]
        return set
    def emptyNuInSquare(self, square): 
        '''find empty site on square'''
        return [i for i in self.full if not i in self.getNuInSquare(square)]
    def nuInSquare(self, square):
        '''find mark site on square'''
        return [i for i in self.full if i in self.getNuInSquare(square)]

    def whichSquare(self, pos):
        return (pos[0]/3*3 + pos[1]/3 + 1) 

    #rule number 1
    def ruleCheckRowColumnSquare(self, pos):
        row = pos[0]
        column = pos[1]
        square = self.whichSquare([row, column])
        rowChance = self.emptyNuInRow(row)
        columnSet = self.nuInColumn(column)
        squareSet = self.nuInSquare(square)
        print rowChance
        print columnSet
        print squareSet
        print pos 
        print square 
        for i in columnSet:
            if i in rowChance:
                rowChance.remove(i)
        for i in squareSet:
            if i in rowChance:
                rowChance.remove(i)
        if len(rowChance) == 1:
            self.sudoku[row][column] = rowChance[0]
            self.printSudoku()
        elif len(rowChance) == 0:
            print '#ERR#'
        else:
            return
        
    #rule number 2
    def ruleOnlyOneNuInLine(self):
        '''every line/column has one "9"'''

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

    de.printSudoku()
    for i in range(0, 9):
        for j in range(0, 9):
            if test[i][j] == 0:
                de.ruleCheckRowColumnSquare([i, j])
    
