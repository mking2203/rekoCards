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

fileDir = os.path.join(actDir, 'files')

#reko.Loadfile(os.path.join(actDir, 'files', 'Aquarium.REKO') , output)
#pc8.Loadfile(os.path.join(actDir, 'files', 'Dogs1.RKP') , output)
#pc16.Loadfile(os.path.join(actDir, 'files', 'TinTin.RKP') , output)
#pc24.Loadfile(os.path.join(actDir, 'files', 'BorisCards1.rkp') , output)
