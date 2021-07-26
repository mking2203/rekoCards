import io
import os
import re
import pathlib
import time

# test for files
import reko
import pc8
import pc16
import pc24

# actual path
actDir = pathlib.Path().resolve()

#create output folder
output = os.path.join(actDir,'output')
if not os.path.exists(output):
    os.mkdir(output)

# files folder
fileDir = os.path.join(actDir, 'files')

# enumerate all reko files
for f in os.listdir(fileDir):
    if re.search('.REKO', f.upper()):
        reko.Loadfile(os.path.join(actDir, 'files', f) , output)
        time.sleep(2)

for f in os.listdir(fileDir):
    if re.search('.rkp', f.lower()):

        f1 = open(os.path.join(actDir, 'files', f),'rb')
        data = f1.read(10)
        f1.close()

        ty = data[:4].decode("utf-8")

        if(ty == 'PCRE'):
            y = data[6]
            if y == 68:
                pc8.Loadfile(os.path.join(actDir, 'files', f) , output)
            elif y == 0:
                pc16.Loadfile(os.path.join(actDir, 'files', f) , output)
            else:
                print('File ???' + f)
        elif ty == 'PCRK':
            pc24.Loadfile(os.path.join(actDir, 'files', f) , output)
        else:
            print('File ???' + f)

        time.sleep(4)

