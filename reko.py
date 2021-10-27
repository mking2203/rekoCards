import io
import os
import re
import pathlib

import BITMAP_File

class Reko:

    data = []
    colorDeep = 0
    height = 0
    width = 0
    cardsCount = 0
    reko = ''
    bodySize = 0
    cardSize = 0
    startData = 0
    mode = 0
    HAM = False

    colorPalette = []
    cards = []

    def toLong(self, start):
        return self.data[start] * 2**24 + self.data[start+1] * 2**16 + self.data[start+2] * 2**8 + self.data[start+3]

    def toInt(self, start):
        return self.data[start] * 2**8 + self.data[start+1]

    def __init__(self, data):

        # header contains 22 bytes

        self.data = data

        self.reko = self.data[:4].decode("utf-8") # REKO

        self.bodySize = self.toLong(4)
        self.cardSize = self.toLong(8)

        self.height = self.toInt(12)
        self.width = self.toInt(14)

        self.mode = self.toLong(16)

        self.colorDeep = self.data[20]
        self.cardsCount = self.data[21]

        self.HAM = False
        if self.mode & 0x0800 != 0:
            self.HAM = True

        print('Cardset: ' + str(self.cardsCount) + ' cards / ' + str(2**self.colorDeep) + ' colors')
        if(self.HAM):
            print('using HAM mode')
        else:
            print('using normal mode')

        if not self.HAM:
            colorsCount = 2**self.data[20] # Normal
        else:
            colorsCount = 2**(self.data[20]-2) # HAM

        # data palette starts after header
        start = 22

        # reset color table
        self.colorPalette = []

        # palette is RGB
        for c in range(colorsCount):
            cls = []
            for i in range(3):
                cls.append (self.data[start + (c*3) + i])

            self.colorPalette.append(cls)

        # data for cards behind palette info
        self.startData = 22 + (colorsCount * 3)

        # read data
        point = self.startData

        for crd in range(self.cardsCount):

            bArr = []

            for l in range(self.height):

                # read bit by bit, highest first for each, then next bit...
                old = []
                new = []

                # copy data
                for x in range(11 * self.colorDeep):
                    old.append(self.data[point])
                    point = point + 1

                # new data
                for x in range(self.width):
                    new.append(0)

                bit = 0
                cnt = 0

                for b in range(self.colorDeep):
                    for dx in range(self.width):

                        if bit == 0:
                            bit = 128
                        elif bit == 128:
                            bit = 64
                        elif bit == 64:
                            bit = 32
                        elif bit == 32:
                            bit = 16
                        elif bit == 16:
                            bit = 8
                        elif bit == 8:
                            bit = 4
                        elif bit == 4:
                            bit = 2
                        elif bit == 2:
                            bit = 1
                        elif bit == 1:
                            bit = 128
                            cnt = cnt + 1

                        if (old[cnt] & bit) != 0:
                            new[dx] = new[dx] | pow(2,b)

                aktCol = [0,0,0]
                for i in range(self.width):
                    if self.HAM:

                        # HAM encoding
                        v = int(new[i])

                        vm = (v & 0x3F) << 2
                        m = (v & 0xC0) >> 6

                        if i==0:
                            val = self.colorPalette[v & 0x3F]
                            aktCol[0] = val[0]
                            aktCol[1] = val[1]
                            aktCol[2] = val[2]
                        else:
                            if m == 0:
                                val = self.colorPalette[v & 0x3F]
                                aktCol[0] = val[0]
                                aktCol[1] = val[1]
                                aktCol[2] = val[2]
                            elif m == 1: # Blue
                                aktCol[2] = vm
                            elif m == 2: # Red
                                aktCol[0] = vm
                            elif m == 3: # Green
                                aktCol[1] = vm

                    else:

                        # normal encoding
                        v = int(new[i])
                        aktCol = self.colorPalette[v]

                    bArr.append(aktCol[0])
                    bArr.append(aktCol[1])
                    bArr.append(aktCol[2])

            self.cards.append(bArr)

# ---------------------------------- MAIN ----------------------------------

def Loadfile(inputFile, outputPath):

    print('Open card file: ' + os.path.basename(inputFile))

    # delete old results
    for f in os.listdir(outputPath):
        if re.search('.tga', f):
            os.remove(os.path.join(outputPath, f))
    for f in os.listdir(outputPath):
        if re.search('.jpg', f):
            os.remove(os.path.join(outputPath, f))
    for f in os.listdir(outputPath):
        if re.search('.bmp', f):
            os.remove(os.path.join(outputPath, f))

    # read data from file
    f = open(inputFile,'rb')
    data = f.read()
    f.close()

    # parse the  data
    reko = Reko(data)

    # generate gfx for the cards
    cnt = 0
    for crd in reko.cards:

        # write file
        fileName = 'Card_' + str(cnt + 1).zfill(2) +'.bmp'
        saveFile = os.path.join(outputPath, fileName)

        BITMAP_File.writeFile(saveFile, crd, reko.width, reko.height)

        # next picture
        cnt = cnt + 1
