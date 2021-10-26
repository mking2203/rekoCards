import sys
import io
import os

import re
import pathlib

import reko
import pc8
import pc16
import pc24

# ---------------------------- MAIN ----------------------------

if len(sys.argv) < 2:
    print('you have specified no argument')
    sys.exit()

# get the filename
file = sys.argv[1]
print('try to open file ' + file)

# check file exist
if not os.path.exists(file):
    print('card file does not exist')
    sys.exit()

# actual path
actDir = pathlib.Path().resolve()

# create output folder
output = os.path.join(actDir,'output')
if not os.path.exists(output):
    os.mkdir(output)
# delete output folder
for f in os.listdir(output):
    os.remove(os.path.join(output, f))

#detect the file type (read 10 bytes)
f1 = open(file,'rb')
data = f1.read(10)
f1.close()

# get the type
ty = data[:4].decode("utf-8")

if(ty == 'PCRE'):
    y = data[6]
    if y == 68:
        print ('detect 8 bit RKP file')
        pc8.Loadfile(file,output)
    elif y == 0:
        print ('detect 16 bit RKP file')
        pc16.Loadfile(file,output)
    else:
        print('PCRE type error ' + f)
        sys.exit()
elif ty == 'PCRK':
    print ('detect 24 bit RKP file')
    pc24.Loadfile(file,output)
elif ty == 'REKO':
    print ('detect REKO file')
    reko.Loadfile(file,output)
else:
    print('file type error ' + f)
    sys.exit()


