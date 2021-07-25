import io
import os
import re
import pathlib

import TGA_File

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

    def __init__(self, data):

        # header contains 22 bytes

        self.data = data

        self.reko = self.data[:4].decode("utf-8") # REKO

        self.bodySize = self.data[4]*pow(2,24) + self.data[5]*pow(2,16) + self.data[6]*pow(2,8) + self.data[7]
        self.cardSize = self.data[8]*pow(2,24) + self.data[9]*pow(2,16) + self.data[10]*pow(2,8) + self.data[11]

        self.height = self.data[12]*pow(2,8) + self.data[13]
        self.width = self.data[14]*pow(2,8) + self.data[15]

        self.mode = self.data[16]*pow(2,24) + self.data[17]*pow(2,16) + self.data[18]*pow(2,8) + self.data[19]
        self.colorDeep = self.data[20]
        self.cardsCount = self.data[21]

        self.HAM = False
        if self.mode & 0x0800 != 0:
            self.HAM = True

        print('Cardset: ' + str(self.cardsCount) + ' cards / ' + str(pow (2,self.colorDeep)) + ' colors')
        if(self.HAM):
            print('using HAM mode')
        else:
            print('using normal mode')

        if not self.HAM:
            colorsCount = pow(2,self.data[20]) # Normal
        else:
            colorsCount = pow(2,self.data[20]-2) # HAM

        # data palette starts after header
        start = 22

        # palette is RGB
        for c in range(colorsCount):
            cls = []
            for i in range(3):
                cls.append (self.data[start + (c*3) + i])

            self.colorPalette.append(cls)

        # data for cards behind palette info
        self.startData = 22 + (colorsCount * 3)

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
pth = 'Aquarium.REKO'

# working (4 bit color...)
#pth = 'DragonsLair_ECS.REKO'

f = open(pth,'rb')
data = f.read()
f.close()

reko = Reko(data)
point = reko.startData

for crd in range(reko.cardsCount):

    bArr = []

    for l in range(reko.height):

        # read bit by bit, highest first for each, then next bit...
        old = []
        new = []

        # copy data
        for x in range(11 * reko.colorDeep):
            old.append(reko.data[point])
            point = point + 1

        # new data
        for x in range(reko.width):
            new.append(0)

        bit = 0
        cnt = 0

        for b in range(reko.colorDeep):
            for dx in range(reko.width):

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

        for i in range(reko.width):

            if reko.HAM:

                # HAM encoding
                v = int(new[i])

                vm = (v & 0x3F) << 2
                m = (v & 0xC0) >> 6

                if i==0:
                    aktCol = reko.colorPalette[v & 0x3F]
                else:
                    if m == 0:
                        aktCol = reko.colorPalette[v & 0x3F]
                    elif m == 1: # B
                        aktCol[2] = vm
                    elif m == 2: # R
                        aktCol[0] = vm
                    elif m == 3: # G
                        aktCol[1] = vm

            else:

                # normal encoding
                v = int(new[i])
                aktCol = reko.colorPalette[v]

            bArr.append(aktCol[2])
            bArr.append(aktCol[1])
            bArr.append(aktCol[0])

    bb = bytes(bArr)

    # write file
    fileName = 'Card_' + str(crd + 1).zfill(2) +'.tga'
    saveFile = os.path.join(output, fileName)

    TGA_File.writeFile(saveFile, bb, reko.width, reko.height)