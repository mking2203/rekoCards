import io
import os
import re
import pathlib

import JPG_File

# this type of card sets contains JPG's. Since I did not find any documentation
# it's just a reverse engineering

class PC:

    data = []
    colorDeep = 0
    height = 0
    width = 0
    cardsCount = 0
    pc_id = ''

    startData = 0

    cards = []

    def __init__(self, data):

        # header contains ?? bytes

        self.data = data

        self.pc_id = self.data[:5].decode("utf-8") # PCRKP

        self.width = self.data[19] * pow(2,24) + self.data[18] * pow(2,16) + self.data[17] * pow(2,8) + self.data[16]
        self.height = self.data[23] * pow(2,24) + self.data[22] * pow(2,16) + self.data[21] * pow(2,8) + self.data[20]
        self.colorDeep = self.data[27] * pow(2,24) + self.data[26] * pow(2,16) + self.data[25] * pow(2,8) + self.data[24]
        self.cardsCount = self.data[31] * pow(2,24) + self.data[30] * pow(2,16) + self.data[29] * pow(2,8) + self.data[28]

        print('PC Cardset: ' + str(self.cardsCount) + ' cards / ' + str(pow (2,self.colorDeep)) + ' colors')

        self.startData = 0x450 # always ??

        # read data, all images are JPG's
        start = self.startData

        for crd in range(self.cardsCount):

            # 4 bytes for the length
            leng = data[start+3] * pow(2,24) + data[start+2] * pow(2,16) + data[start+1] * pow(2,8) + data[start]

            start = start + 4
            ende = start + leng

            # get the image
            pic = []
            for i in range(start, ende):
                pic.append(data[i])

            start = start + leng

            self.cards.append(pic)



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

# read data from file
pth = 'BorisCards1.rkp'

f = open(pth,'rb')
data = f.read()
f.close()

# parse the  data
pcCard = PC(data)

# generate JPG for the cards
cnt = 0
for crd in pcCard.cards:

    # write file
    fileName = 'Card_' + str(cnt + 1).zfill(2) +'.jpg'
    saveFile = os.path.join(output, fileName)

    JPG_File.writeFile(saveFile, crd)

    # next picture
    cnt = cnt + 1



