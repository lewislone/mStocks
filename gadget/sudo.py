# -*- coding: utf-8 -*-
import os

class deSudoku:
    def __init__(self, sudoku):
        print("init...")
        self.sudoku = sudoku 
        self.full = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.maybe={}

    def __del(self, set1, set2):
        for i in set2:
            if i in set1:
                set1.remove(i)
        return set1
    def __add(self, set1, set2):
        return set1 + set2
    def __and(self, set1, set2):#the same item between set1 and set2
        return [i for i in set1 if (i in set2 and i != 0)]
    def __xor(self, set1, set2):#items in set1 but not in set2
        return [i for i in set1 if i not in set2]
    def __or(self, set1, set2):#all items of set1 and set2 without dulplicate
        return self.__add(self.__and(set1, set2), self.__xor(set1, set2))

    def getID(self, pos):
        return str(pos[0])+str(pos[1])
    
    def printSudoku(self):
        print('###########################')
        for i in range(0, 9):
            print(self.sudoku[i])
        print('###########################\n')

    def nuInRow(self, row): 
        '''find site taken on row'''
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
        '''find site taken on column'''
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
        '''find site taken on square'''
        return [i for i in self.full if i in self.getNuInSquare(square)]

    def whichSquare(self, pos):
        return (pos[0]/3*3 + pos[1]/3 + 1) 

    def allPosInSquare(self, sequare):
        seq = sequare-1
        return ((seq/3*3, seq%3*3),(seq/3*3, seq%3*3+1),(seq/3*3, seq%3*3+2), \
                (seq/3*3+1, seq%3*3),(seq/3*3+1, seq%3*3+1),(seq/3*3+1, seq%3*3+2), \
                (seq/3*3+2, seq%3*3),(seq/3*3+2, seq%3*3+1),(seq/3*3+2, seq%3*3+2))
    def allPosInRow(self, row):
        return ((row, 0), (row, 1), (row, 2), \
                (row, 3), (row, 4), (row, 5), \
                (row, 6), (row, 5), (row, 6))
    def allPosInColumn(self, column):
        return((0, column), (1, column), (2, column), \
                (3, column), (4, column), (5, column), \
                (6, column), (7, column), (8, column))

    def findSameMaybe(self, index, type):
        allBe = []
        allSame = {}
        if type == 1:
            fun = self.allPosInRow
        elif type == 2:
            fun = self.allPosInColumn
        elif type == 3:
            fun = self.allPosInSquare
        else:
            fun = self.allPosInRow
            
        for pos in fun(index):
            if self.sudoku[pos[0]][pos[1]] != 0:
                continue
            be = self.maybe[self.getID(pos)+'yes']
            allBe.append(be)
        for pos in fun(index):
            if self.sudoku[pos[0]][pos[1]] != 0:
                continue
            be = self.maybe[self.getID(pos)+'yes']
            beKey = str(be)
            if beKey not in allSame.keys():
                allSame[beKey] = 1
                allSame[beKey+'pos'] = [pos]
            else:
                allSame[beKey] += 1
                allSame[beKey+'pos'].append(pos)

        br = 0
        for pos in fun(index):
            if self.sudoku[pos[0]][pos[1]] != 0:
                continue
            be = self.maybe[self.getID(pos)+'yes']
            #if pos == (3,3):
            #    print allBe, allSame[str(be)]
            #    print allSame
            if len(be) == allSame[str(be)]:
                for pos2 in fun(index):
                    if self.sudoku[pos2[0]][pos2[1]] != 0:
                        continue
                    if pos2 not in allSame[str(be)+'pos']:
                        #print allSame
                        if self.maybe[self.getID(pos2)+'yes'] != self.__xor(self.maybe[self.getID(pos2)+'yes'], be):
                            self.maybe[self.getID(pos2)+'yes'] = self.__xor(self.maybe[self.getID(pos2)+'yes'], be)
                            self.maybe[self.getID(pos2)+'yes'].sort()
                            br = 1
                        if self.maybe[self.getID(pos2)+'no'] != self.__xor(self.full, self.maybe[self.getID(pos2)+'yes']):
                            self.maybe[self.getID(pos2)+'no'] = self.__xor(self.full, self.maybe[self.getID(pos2)+'yes'])
                            self.maybe[self.getID(pos2)+'no'].sort()
                            br = 1
            if br == 1:
                break
                    
        
    def getMaybeAndNot2(self, index):
        #row
        self.findSameMaybe(index, 1)
        #column
        #self.findSameMaybe(index, 2)
        #square
        #self.findSameMaybe(index+1, 3)

    def getMaybeAndNot(self, pos):
        square = self.whichSquare(pos)
        #get likely 
        maybeRow = self.emptyNuInRow(pos[0])
        maybeColumn = self.emptyNuInColumn(pos[1])
        maybeSquare = self.emptyNuInSquare(square)
        likely = self.__and(maybeSquare, self.__and(maybeRow, maybeColumn))
        likely.sort()
        if self.getID(pos)+'yes' not in self.maybe.keys():
            self.maybe[self.getID(pos)+'yes'] = likely
        elif len(likely) < len(self.maybe[self.getID(pos)+'yes']):
            self.maybe[self.getID(pos)+'yes'] = likely

        if pos == [2, 11]: 
                print pos
                print maybeRow
                print maybeColumn
                print maybeSquare
                print likely

        #get unlikely
        noRow = self.nuInRow(pos[0])
        noColumn = self.nuInColumn(pos[1])
        noSquare = self.nuInSquare(square)
        unlikely = [x for x in set(self.__add(self.__add(noRow, noColumn), noSquare))] 
        self.maybe[self.getID(pos)+'no'] = unlikely

        if pos == [2, 11]: 
                print pos
                print noRow
                print noColumn
                print noSquare
                print unlikely 
        if pos == [9, 11]:
            print pos, self.maybe[self.getID(pos)+'yes'], self.maybe[self.getID(pos)+'no']


    # if likely number is only one we get the answer
    def tryFill(self, pos):
        #print 'tryFill',pos
        row = pos[0]
        column = pos[1]
        be = self.maybe[self.getID(pos)+'yes']
        notbe = self.maybe[self.getID(pos)+'no']

        if len(be) == 1:
            print be, pos
            self.sudoku[row][column] = be[0]
            self.printSudoku()
            return

       # tmp = self.full 
       # #row 
       # for p in self.allPosInRow(row):
       #     if self.sudoku[p[0]][p[1]] != 0:
       #         continue
       #     if not self.getID(p)+'no' in self.maybe.keys():
       #         break
       #     if p[0] != row and p[1] != column:
       #         tmp = self.__and(tmp, self.maybe[self.getID(p)+'no'])
       #     if len(tmp) > 1:
       #         tmp = self.__and(tmp, self.maybe[self.getID(p)+'yes'])

       #     if len(tmp) == 1:
       #         self.sudoku[row][column] = tmp[0]
       #         self.printSudoku()
       # 
       # tmp = self.full 
       # #column
       # for p in self.allPosInColumn(column):
       #     if self.sudoku[p[0]][p[1]] != 0:
       #         continue
       #     if not self.getID(p)+'no' in self.maybe.keys():
       #         break
       #     if p[0] != row and p[1] != column:
       #         tmp = self.__and(tmp, self.maybe[self.getID(p)+'no'])
       #     if len(tmp) > 1:
       #         tmp = self.__and(tmp, self.maybe[self.getID(p)+'yes'])

       #     if len(tmp) == 1:
       #         self.sudoku[row][column] = tmp[0]
       #         self.printSudoku()

        tmp = self.full 
        #square
        for p in self.allPosInSquare(self.whichSquare(pos)):
            if self.sudoku[p[0]][p[1]] != 0:
                continue
            #print p
            if not (self.getID(p)+'no' in self.maybe.keys()):
                break
            if not (p[0] == row and p[1] == column):
                #print 'no', self.maybe[self.getID(p)+'no']
                tmp = self.__and(tmp, self.maybe[self.getID(p)+'no'])

        #print tmp
        if len(tmp) > 0:
            tmp = self.__and(tmp, self.maybe[self.getID(pos)+'yes'])
        #print 'yes', self.maybe[self.getID(pos)+'yes']
        #print tmp

        if len(tmp) == 1:
            print '###', pos, tmp
            for p in self.allPosInSquare(self.whichSquare(pos)):
                if self.sudoku[p[0]][p[1]] != 0:
                    continue
                if not (self.getID(p)+'no' in self.maybe.keys()):
                    break
                if not (p[0] == row and p[1] == column):
                    print 'no', p, self.maybe[self.getID(p)+'no']
            print 'yes', pos, self.maybe[self.getID(pos)+'yes']

            self.maybe[self.getID(pos)+'yes'] = [tmp[0]]
            self.maybe[self.getID(pos)+'no'] = [i for i in self.full if i != tmp[0]]
            self.sudoku[row][column] = tmp[0]
            self.printSudoku()

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
        
        common1 = self.__and(row1, row2)
        common2 = self.__and(tmpColumn1, tmpColumn2)
        commonRow = self.__and(common1, common2)

        common1 = self.__and(tmpRow1, tmpRow2)
        common2 = self.__and(column1, column2)
        commonColumn = self.__and(common1, common2)

        if row == 9 and column == 9:
            self.printSudoku()
            print (pos, otherRow1, otherRow2, otherColumn1, otherColumn2)
            print tmpRow1
            print tmpRow2
            print tmpColumn1
            print tmpColumn2

        common = self.__and(row1, column1)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn2] != 0 and self.sudoku[otherRow2][column] != 0 and self.sudoku[otherRow2][otherColumn2] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()
        common = self.__and(row2, column1)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn2] != 0 and self.sudoku[otherRow1][column] != 0 and self.sudoku[otherRow1][otherColumn2] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()
        common = self.__and(row1, column2)
        if len(common) == 1 and common[0] not in self.nuInSquare(self.whichSquare(pos)) \
                    and self.sudoku[row][otherColumn1] != 0 and self.sudoku[otherRow2][column] != 0 and self.sudoku[otherRow2][otherColumn1] != 0:
           self.sudoku[row][column] = common[0]
           print((pos, self.sudoku[row][column]))
           self.printSudoku()
        common = self.__and(row2, column2)
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
            [0, 0, 1, 0, 0, 7, 0, 0, 5],
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
                  if de.sudoku[i][j] == 0:
                     de.getMaybeAndNot([i, j])
                     #de.tryFill([i, j])
                     #de.ruleCheckRowColumnSquare([i, j])
                     #de.ruleOnlyOneNuInLine([i, j])

          for i in range(0, 9):
              for j in range(0, 9):
                  if de.sudoku[i][j] == 0:
                     de.tryFill([i, j])

          for i in range(0, 9):
              de.getMaybeAndNot2(i)
    
          #de.tryFill([2, 8])
          #de.tryFill([4, 5])
          #de.tryFill([5, 0])
          #de.tryFill([5, 3])
