# -*- coding: utf-8 -*-
import sys
import os
import glob
import sys
import os
import glob
#Path_current=sys.argv[0]
#N_iter=sys.argv[1]
#Name_Rmapfile=sys.argv[2]
Path_current='/home/tyhuang/FACEmars'
N_iter=100
Name_Rmapfile='Rmap_beswarrest.nii'

# 分別讀取 Path_current下面的cont與exp資料夾內的MARS結果資料夾，直接從各資料夾中讀取名稱為 Name_Rmapfile(Rmap_beswarrest.nii)的檔案
list_control = glob.glob(Path_current + '/cont/*')
list_experim = glob.glob(Path_current + '/exp/*')

# 列出control內所有的影像路徑
str_control=''
for ii in list_control:
    str_control=str_control+ ii +'/'+ Name_Rmapfile +' '

# 把所有control受試者的Rmap合併成一個四維的Rmaps
str_OSins='fslmerge -t '+ Path_current + '/contRmaps '+ str_control
os.system(str_OSins)

# 列出Expriment內所有的影像路徑
str_experim=''
for ii in list_experim:
    str_experim=str_experim+ ii +'/'+ Name_Rmapfile +' '


# 把所有Expriment受試者的Rmap合併成一個四維的Rmaps
str_OSins='fslmerge -t '+ Path_current + '/expRmaps '+ str_experim
os.system(str_OSins)

# 做出control的One sample t-test結果
str_OSins='randomise -i %s/contRmaps -o %s/contTwottst -1  -n %d --T2'%(Path_current ,Path_current ,N_iter)
os.system(str_OSins)

# 做出Expriment的One sample t-test結果
str_OSins='randomise -i %s/expRmaps  -o %s/contTwottst -1  -n %d --T2'%(Path_current ,Path_current ,N_iter)
os.system(str_OSins)

# 把兩個群組的Rmaps合併成一個，並且由design.mat決定群組
str_OSins='fslmerge -t allRmaps '+ Path_current + '/contRmaps ' + Path_current + '/expRmaps '
os.system(str_OSins)

# 若兩組資料只是單純的兩群不同受試者比較Two-Sample Unpaired T-test，而非Two-Sample Paired T-test (Paired Two-Group Difference)
# 可以用 design_ttest2 檔案名稱 群組A數目 群組B數目 來建立design.mat以及design.con
# design.mat是GLM用來分辨不同群組的矩陣。design.con是不同群組之間的contrast(譬如說A >B 或A<B)
str_OSins='design_ttest2 %s/design %d %d'%(Path_current , len(list_control ),len(list_experim ))
os.system(str_OSins)

# 執行兩群組之間的Two sample t-test
str_OSins='randomise -i %s/allRmaps -o %s/resultTwottst -d design.mat -t design.con --T2 -n %d'%(Path_current,Path_current  ,N_iter)
os.system(str_OSins)
