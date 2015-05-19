# -*- coding: utf-8 -*-
import os

class deSudoku:
    def __init__(self, sudoku):
        print("init...")
        self.sudoku = sudoku 
        self.full = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __del(self, set1, set2):
        for i in set2:
            if i in set1:
                set1.remove(i)
        return set1
    def __add(self, set1, set2):
        return set1 + set2   
    def __or(self, set1, set2):
        return [i for i in set1 if (i in set2 and i != 0)] 
    def __xor(self, set1, set2):
        return [i for i in set1 if i not in set2] 
    
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
        set += self.sudoku[((square-1)/3)*3][(((square-1)%3)*3) : (3+((square-1)%3)*3)]
        set += self.sudoku[((square-1)/3)*3+1][(((square-1)%3)*3) : (3+((square-1)%3)*3)]
        set += self.sudoku[((square-1)/3)*3+2][(((square-1)%3)*3) : (3+((square-1)%3)*3)]
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
            print('#rule number 1 ERR#')
        else:
            return
        
    #rule number 2
    def ruleOnlyOneNuInLine(self, pos):
        '''every line/column has one "9"'''
        row = pos[0]
        column = pos[1]
        if (row-1)/3 != row/3:
            otherRow1 = row + 1
            otherRow2 = row + 2
        elif (row+1)/3 != row/3:
            otherRow1 = row - 1
            otherRow2 = row - 2
        else:
            otherRow1 = row - 1
            otherRow2 = row + 1 

        if (column-1)/3 != column/3:
            otherColumn1 = column + 1
            otherColumn2 = column + 2
        elif (column+1)/3 != column/3:
            otherColumn1 = column - 1
            otherColumn2 = column - 2
        else:
            otherColumn1 = column - 1
            otherColumn2 = column + 1

        row1 = [i for i in self.sudoku[otherRow1]]
        row2 = [i for i in self.sudoku[otherRow2]]
        column1 = [self.sudoku[i][otherColumn1] for i in range(0, 9)]
        column2 = [self.sudoku[i][otherColumn2] for i in range(0, 9)]
        del(row1[min(column, otherColumn1, otherColumn2) : max(column, otherColumn1, otherColumn2)+1])
        del(row2[min(column, otherColumn1, otherColumn2) : max(column, otherColumn1, otherColumn2)+1])
        del(column1[min(row, otherRow1, otherRow2) : max(row, otherRow1, otherRow2)+1])
        del(column2[min(row, otherRow1, otherRow2) : max(row, otherRow1, otherRow2)+1])

        if self.sudoku[otherRow1][column] != 0:
           tmpRow1 = self.full 
        else:
           tmpRow1 = row1 
        if self.sudoku[otherRow2][column] != 0:
           tmpRow2 = self.full 
        else:
           tmpRow2 = row2 
           

        if self.sudoku[row][otherColumn1] != 0:
           tmpColumn1 = self.full 
        else:
           tmpColumn1 = column1 
        if self.sudoku[row][otherColumn2] != 0:
           tmpColumn2 = self.full 
        else:
           tmpColumn2 = column2
        
        common1 = self.__or(row1, row2)
        common2 = self.__or(tmpColumn1, tmpColumn2)
        commonRow = self.__or(common1, common2)

        common1 = self.__or(tmpRow1, tmpRow2)
        common2 = self.__or(column1, column2)
        commonColumn = self.__or(common1, common2)

        if row == 9 and column == 9:
            self.printSudoku()
            print (pos, otherRow1, otherRow2, otherColumn1, otherColumn2)
            print tmpRow1
            print tmpRow2
            print tmpColumn1
            print tmpColumn2

        common = self.__or(row1, column1)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn2] != 0 and self.sudoku[otherRow2][column] != 0 and self.sudoku[otherRow2][otherColumn2] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()
        common = self.__or(row2, column1)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn2] != 0 and self.sudoku[otherRow1][column] != 0 and self.sudoku[otherRow1][otherColumn2] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()
        common = self.__or(row1, column2)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn1] != 0 and self.sudoku[otherRow2][column] != 0 and self.sudoku[otherRow2][otherColumn1] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()
        common = self.__or(row2, column2)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn1] != 0 and self.sudoku[otherRow1][column] != 0 and self.sudoku[otherRow1][otherColumn1] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()

        for i in commonRow:
            if i not in self.nuInRow(row) and i not in self.nuInColumn(column) and i not in self.nuInSquare(self.whichSquare(pos)):
                self.sudoku[row][column] = commonRow[0]
                print((pos, self.sudoku[row][column]))
                self.printSudoku()
        for i in commonColumn:
            if i not in self.nuInRow(row) and i not in self.nuInColumn(column) and i not in self.nuInSquare(self.whichSquare(pos)):
                self.sudoku[row][column] = commonColumn[0]
                print((pos, self.sudoku[row][column]))
                self.printSudoku()


if __name__ == '__main__':
    test = [
            [9, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 7, 0, 0, 0, 5],
            [0, 6, 0, 0, 0, 0, 0, 9, 0],
            [7, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 4, 0, 8, 0, 0, 0, 2],
            [0, 5, 0, 0, 3, 4, 0, 0, 0],
            [0, 0, 0, 8, 0, 0, 4, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 6, 0],
            [0, 7, 2, 0, 0, 0, 0, 0, 9]
            ]
    de = deSudoku(test)

    de.printSudoku()
    while True:
          for i in range(0, 9):
              for j in range(0, 9):
                  if test[i][j] == 0:
                     de.ruleCheckRowColumnSquare([i, j])
                     de.ruleOnlyOneNuInLine([i, j])
    
