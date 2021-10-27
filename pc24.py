import io
import os
import re
import pathlib

import JPG_File

# this type of card sets contains JPG's

class PC24:

    data = []
    colorDeep = 0
    height = 0
    width = 0
    cardsCount = 0
    bodySize = 0
    cardSize = 0

    creator = ''
    mail = ''
    website = ''
    comment = ''
    category = ''
    date = ''

    pc_id = ''

    startData = 0

    cards = []

    def toLong(self, start):
        return self.data[start+3] * 2**24 + self.data[start+2] * 2**16 + self.data[start+1] * 2**8 + self.data[start]

    def getString(self, data):
        strData = ''

        for b in data:
            if (b != 0):
                strData = strData + chr(b)
            else:
                break

        return strData

    def __init__(self, data):

        # header contains ?? bytes

        self.data = data

        self.pc_id = self.data[:5].decode("utf-8") # PCRKP

        self.cardSize = self.toLong(8)
        self.bodySize = self.toLong(12)

        self.width = self.toLong(16)
        self.height = self.toLong(20)
        self.colorDeep = self.toLong(24)
        self.cardsCount = self.toLong(28)

        a = 36
        self.creator = self.getString(data[a:a+255])
        a = a + 256
        self.mail = self.getString(data[a:a+255])
        a = a + 256
        self.website = self.getString(data[a:a+255])
        a = a + 256
        self.comment = self.getString(data[a:a+255])
        a = a + 256
        self.category = self.getString(data[a:a+19])
        a = a + 20
        self.date = self.getString(data[a:a+20])

        print('PC Cardset: ' + str(self.cardsCount) + ' cards / ' + str(pow (2,self.colorDeep)) + ' colors')
        print('Creator: ' + self.creator)

        self.startData = 0x450 # always ??

        # read data, all images are JPG's
        start = self.startData

        self.cards = []

        for crd in range(self.cardsCount):

            # 4 bytes for the length
            leng = self.toLong(start)

            start = start + 4
            ende = start + leng

            # get the image
            pic = []
            for i in range(start, ende):
                pic.append(data[i])

            start = start + leng

            self.cards.append(pic)

# ---------------------------------- MAIN ----------------------------------

def Loadfile(inputFile, outputPath):

    print('Open card file PC24: ' + os.path.basename(inputFile))

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

    f = open(inputFile,'rb')
    data = f.read()
    f.close()

    # parse the  data
    pcCard = PC24(data)

    # generate JPG for the cards
    cnt = 0
    for crd in pcCard.cards:

        # write file
        fileName = 'Card_' + str(cnt + 1).zfill(2) +'.jpg'
        saveFile = os.path.join(outputPath, fileName)

        JPG_File.writeFile(saveFile, crd)

        # next picture
        cnt = cnt + 1

