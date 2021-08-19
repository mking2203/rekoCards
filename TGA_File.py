####################################################
#                                                  #
#  Helper modul to save the data to a TGA file     #
#                                                  #
####################################################

import io

def writeFile(SaveFile, Data, Width, Height):

    # prepare TGA header
    bArr =[]

    bArr.append(0)
    bArr.append(0)
    bArr.append(2)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(Width)
    bArr.append(0)
    bArr.append(Height)
    bArr.append(0)

    bArr.append(24)
    bArr.append(32)

    # add picture data
    x = 0
    b1 = 0  # R
    b2 = 0  # G

    for b in Data:
        x = x + 1
        if x == 1: b1 = b
        if x == 2: b2 = b

        if x == 3:
            # for the TGA we need BGR
            bArr.append(b)
            bArr.append(b2)
            bArr.append(b1)
            x = 0

    # convert to byte array
    bBytes = bytes(bArr)

    f = open(SaveFile,'wb')
    f.write(bBytes)
    f.close()
