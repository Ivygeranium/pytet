from matrix import *
from random import *
from enum import Enum
#import LED_display as LMD 

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return
		
    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen
		
    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        self.top = 0
        self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        return

    def printScreen(self):
        array = self.oScreen.get_array()

        for y in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for x in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                if array[y][x] == 0:
                    print("□", end='')
                    #LMD.set_pixel(y, 19-x, 0)
                elif array[y][x] == 1:
                    print("■", end='')
                    #LMD.set_pixel(y, 19-x, 4)
                else:
                    print("XX", end='')
                    #continue
            print()

    def deleteFullLines(self): # To be implemented!!
        sum = 0
        blank_line = Matrix([[0]*(self.oScreen.get_dx()-2*Tetris.iScreenDw)])
        cpoy = 0
        array = self.oScreen.get_array()
        for i in range(self.oScreen.get_dy()-Tetris.iScreenDw):
            for j in range(Tetris.iScreenDw, self.oScreen.get_dx()-Tetris.iScreenDw):
                sum += array[i][j]
                if sum == self.oScreen.get_dx()-2*Tetris.iScreenDw:
                    copy = self.oScreen.clip(0, Tetris.iScreenDw, i, self.oScreen.get_dx()-Tetris.iScreenDw)
                    self.oScreen.paste(copy, 1, Tetris.iScreenDw)
                    self.oScreen.paste(blank_line, 0, Tetris.iScreenDw)
            sum = 0
        return self.oScreen

    def accept(self, key): # To be implemented!!
        if key.isdigit():
            self.idxBlockType = int(key)
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - 2
	    
        self.state = TetrisState.Running
        
        if key == 's':
            self.top += 1
        elif key == 'a':
            self.left -= 1
        elif key == 'd':
            self.left += 1
        elif key == 'w':
            self.idxBlockDegree  = (self.idxBlockDegree + 1 ) % 4

        elif key == ' ':
            while not self.tempBlk.anyGreaterThan(1):
                self.top += 1
                self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
                self.tempBlk = self.tempBlk + self.currBlk
        self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        if self.tempBlk.anyGreaterThan(1):
            if key == 's' or key == ' ':
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'a':
                self.left += 1
            elif key == 'd':
                self.left -= 1  
            elif key == 'w':
                if self.idxBlockDegree == 0:
                    self.idxBlockDegree = 4
                else:
                    self.idxBlockDegree  -= 1                   
                    
        self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk
        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)
        if self.tempBlk.anyGreaterThan(1):
            self.state = TetrisState.Finished
        if self.state == TetrisState.NewBlock:
            self.iScreen = Matrix(self.oScreen)

        self.oScreen = self.deleteFullLines()
        print()

        return self.state

    
