import io
import os
import re
import pathlib

import BITMAP_File

class PC16:

    data = []
    colorDeep = 0
    height = 0
    width = 0
    cardsCount = 0
    pc_id = ''
    pc_id2 = ''
    bodySize = 0
    cardSize = 0
    startData = 0

    cards = []

    def toLong(self, start):
        return self.data[start+3] * 2**24 + self.data[start+2] * 2**16 + self.data[start+1] * 2**8 + self.data[start]

    def toInt(self, start):
        return self.data[start+1] * 2**8 + self.data[start]

    def __init__(self, data):

        # header contains 22 bytes

        self.data = data

        self.pc_id = self.data[:6].decode("utf-8") # PCREKO
        self.pc_id2 = self.data[6:7].decode("utf-8") # 0x00

        self.cardSize = self.toLong(8)
        self.bodySize =  self.toLong(12)

        self.width = self.toInt(16)
        self.height = self.toInt(18)

        self.colorDeep = self.data[20]
        self.cardsCount = self.data[21]

        print('PC Cardset: ' + str(self.cardsCount) + ' cards / ' + str(pow (2,self.colorDeep)) + ' colors')

        self.startData = 22

        # read data

        point = self.startData

        self.cards = []

        for crd in range(self.cardsCount):

            # skip size
            point = point + 4

            byArr = []

            # get the image
            for l in range(self.height):
                for i in range(self.width):

                    v = int(self.toInt(point))
                    point = point + 2

                    r = ((v & 0x7C00) >> 10) << 3
                    g = ((v & 0x03E0) >> 5) << 3
                    b = ((v & 0x001F) << 3)

                    byArr.append(r)
                    byArr.append(g)
                    byArr.append(b)

            self.cards.append(byArr)

# ---------------------------------- MAIN ----------------------------------

def Loadfile(inputFile, outputPath):

    print('Open card file PC16: ' + os.path.basename(inputFile))

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
    pcCard = PC16(data)

    # generate TGA for the cards
    cnt = 0
    for crd in pcCard.cards:

        # write file
        fileName = 'Card_' + str(cnt + 1).zfill(2) +'.bmp'
        saveFile = os.path.join(outputPath, fileName)

        BITMAP_File.writeFile(saveFile, crd, pcCard.width, pcCard.height)

        # next picture
        cnt = cnt + 1