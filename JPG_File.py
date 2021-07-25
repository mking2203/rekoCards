####################################################
#                                                  #
#  Helper modul to save the data to a JPG file     #
#                                                  #
####################################################

import io

def writeFile(SaveFile, Data):

    bArr =[]

    # add picture data
    for b in Data:
        bArr.append(b)

    # convert to byte array
    bBytes = bytes(bArr)

    f = open(SaveFile,'wb')
    f.write(bBytes)
    f.close()
