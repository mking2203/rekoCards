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
    for b in Data:
        bArr.append(b)

    # convert to byte array
    bBytes = bytes(bArr)

    f = open(SaveFile,'wb')
    f.write(bBytes)
    f.close()
