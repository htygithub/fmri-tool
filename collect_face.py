from scipy.io import loadmat
import pandas as pd
import glob
import numpy as np
import shutil
#matfile = loadmat('abide_mars2_0050002_3726')
v1 = pd.read_excel('face_list.xlsx')

files = glob.glob(r'*')
SUB_ID = v1.SUB_ID
DX_GROUP = v1.DX_GROUP
SUB_ID = SUB_ID.tolist()
DX_GROUP = DX_GROUP.tolist()
asd = []
tc = []

for ii in range(len(SUB_ID)):
    print(SUB_ID[ii])
    for f in files:
        if SUB_ID[ii]+'_' in f:
            if DX_GROUP[ii] == 1:
                asd.append(f)
            else:
                tc.append(f)
#for i in range(len(data)):
#    shutil.copy(data[i], 'Z:\\Exp_Data\\105_Lynn\\abide_marsmat\\gooddata\\')
with open('asdlist.txt', 'w') as outfile:
    outfile.write('\n'.join(asd)+'\n')
with open('tclist.txt', 'w') as outfile:
    outfile.write('\n'.join(tc)+'\n')
