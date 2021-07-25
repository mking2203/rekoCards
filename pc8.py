import io
import os
import re
import pathlib

import TGA_File

class PC:

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

    def __init__(self, data):

        # header contains 22 bytes

        self.data = data

        self.pc_id = self.data[:6].decode("utf-8") # PCREKO
        self.pc_id2 = self.data[6:7].decode("utf-8") # D

        self.bodySize = self.data[11] * pow(2,24) + self.data[10] * pow(2,16) + self.data[9] * pow(2,8) + self.data[8]
        self.cardSize = self.data[15] * pow(2,24) + self.data[14] * pow(2,16) + self.data[13] * pow(2,8) + self.data[12]

        self.width = self.data[17] * pow(2,8) + self.data[16]
        self.height = self.data[19] * pow(2,8) + self.data[18]

        self.colorDeep = self.data[20]
        self.cardsCount = self.data[21]

        print('PC Cardset: ' + str(self.cardsCount) + ' cards / ' + str(pow (2,self.colorDeep)) + ' colors')

        self.startData = 22

        # read data

        point = self.startData

        for crd in range(self.cardsCount):

            # skip size
            point = point + 4

            byArr = []
            colorPalette = []

            # each card has a color table
            for cls in range(256):
                v = int(self.data[point + 1] * pow(2,8) + self.data[point])
                colorPalette.append(v)
                point = point + 2

            # get the image
            for l in range(self.height):
                for i in range(self.width):

                    v = int(self.data[point])
                    point = point + 1

                    # get color from table
                    v = colorPalette[v]

                    b = ((v & 0x7C00) >> 10) << 3
                    g = ((v & 0x03E0) >> 5) << 3
                    r = ((v & 0x001F) << 3)

                    byArr.append(r)
                    byArr.append(g)
                    byArr.append(b)

            self.cards.append(byArr)

# ---------------------------------- MAIN ----------------------------------

# actual path
actDir = pathlib.Path().resolve()

#create output folder
output = os.path.join(actDir,'output')
if not os.path.exists(output):
    os.mkdir(output)

# delete old results
for f in os.listdir(output):
    if re.search('.tga', f):
        os.remove(os.path.join(output, f))
for f in os.listdir(output):
    if re.search('.jpg', f):
        os.remove(os.path.join(output, f))

# file to load
pth = 'Dogs1.RKP'

# read data from file
f = open(pth,'rb')
data = f.read()
f.close()

# parse the  data
pcCard = PC(data)

# generate TGA for the cards
cnt = 0
for crd in pcCard.cards:

    # write file
    fileName = 'Card_' + str(cnt + 1).zfill(2) +'.tga'
    saveFile = os.path.join(output, fileName)

    TGA_File.writeFile(saveFile, crd, pcCard.width, pcCard.height)

    # next picture
    cnt = cnt + 1