from scipy.io import loadmat
import pandas as pd
import glob
import numpy as np
import shutil
#matfile = loadmat('abide_mars2_0050002_3726')
v1 = pd.read_csv(r'Phenotypic_V1_0b_preprocessed1.csv',encoding = 'iso-8859-1')
v2 = pd.read_csv(r'ABIDEII_Composite_Phenotypic.csv',encoding = 'iso-8859-1')
#v2=v1[(v1.qc_rater_1 != 'fail') & (v1.qc_anat_rater_2 != 'fail') & \
#      (v1.qc_func_rater_2 != 'fail') & (v1.qc_func_rater_3 != 'fail')]
#data=v2.as_matrix()
#v2 = v1[v1.SRS_RAW_TOTAL>0]
files = glob.glob(r'*')
SUB_ID = v1.SUB_ID.tolist() + v2.SUB_ID.tolist()
DX_GROUP = v1.DX_GROUP.tolist() + v2.DX_GROUP.tolist()
asd = []
tc = []

for ii in range(len(SUB_ID)):
    for f in files:
        if str(SUB_ID[ii]) in f:
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
