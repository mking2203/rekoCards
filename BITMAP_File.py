####################################################
#                                                  #
#  Helper modul to save the data to a BITMAP file  #
#                                                  #
####################################################

import io

def writeFile(SaveFile, Data, Width, Height):

    # prepare BITMAP header
    bArr =[]

    bArr.append(0x42) # BM
    bArr.append(0x4D)

    bArr.append(0) # Dateilänge
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0) # Reserviert
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0x36) # Zeiger auf Daten
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0x28) # Headergröße
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(Width) # Breite
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(Height) # Höhe
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0x01) # Ebenen
    bArr.append(0)

    bArr.append(0x18) # Bits pro Pixel
    bArr.append(0)

    bArr.append(0) # Kompression
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0) # Pixeldaten
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0xC4) # X-Resolution
    bArr.append(0x0E)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0xC4) # Y-Resolution
    bArr.append(0x0E)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0) # Anzahl Farben (0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    bArr.append(0) # Anzahl wichtiger Farben (0)
    bArr.append(0)
    bArr.append(0)
    bArr.append(0)

    # add picture data

    # data to swap color order
    xNr = 0
    b1 = 0
    b2 = 0

    Data.reverse() # mirror horizontal

    for y in range(Height): # each line
        for x in range((Width * 3)-1, -1, -1): # form left to right  (mirror vert.)

            b = Data[(y * Width * 3) + x]

            xNr = xNr + 1
            if xNr == 1: b1 = b
            if xNr == 2: b2 = b

            if xNr == 3:
                # since we inverted the picture turn back the colors
                bArr.append(b)
                bArr.append(b2)
                bArr.append(b1)
                xNr = 0

    # get the size and write to array
    x = len(bArr)

    bArr[5] = int(x / 2**24)
    x = x - (bArr[5] * 2**24)
    bArr[4] = int(x / 2**16)
    x = x - (bArr[4] * 2**16)
    bArr[3] = int(x / 2**8)
    x = x - (bArr[3] * 2**8)
    bArr[2] = x

    # convert to byte array
    bBytes = bytes(bArr)

    f = open(SaveFile,'wb')
    f.write(bBytes)
    f.close()
