import sys
import os
import glob
#Path_current=sys.argv[0]
#N_iter=sys.argv[1]
#Name_Rmapfile=sys.argv[2]
Path_current='/home/tyhuang/FACEmars'
N_iter=100
Name_Rmapfile='Rmap_beswarrest.nii'

# ���OŪ�� Path_current�U����cont�Pexp��Ƨ�����MARS���G��Ƨ��A�����q�U��Ƨ���Ū���W�٬� Name_Rmapfile(Rmap_beswarrest.nii)���ɮ�
list_control = glob.glob(Path_current + '/cont/*')
list_experim = glob.glob(Path_current + '/exp/*')

# �C�Xcontrol���Ҧ����v�����|
str_control=''
for ii in list_control:
    str_control=str_control+ ii +'/'+ Name_Rmapfile +' '

# ��Ҧ�control���ժ̪�Rmap�X�֦��@�ӥ|����Rmaps
str_OSins='fslmerge -t '+ Path_current + '/contRmaps '+ str_control
os.system(str_OSins)

# �C�XExpriment���Ҧ����v�����|
str_experim=''
for ii in list_experim:
    str_experim=str_experim+ ii +'/'+ Name_Rmapfile +' '


# ��Ҧ�Expriment���ժ̪�Rmap�X�֦��@�ӥ|����Rmaps
str_OSins='fslmerge -t '+ Path_current + '/expRmaps '+ str_experim
os.system(str_OSins)

# ���Xcontrol��One sample t-test���G
str_OSins='randomise -i %s/contRmaps -o %s/contTwottst -1  -n %d --T2'%(Path_current ,Path_current ,N_iter)
os.system(str_OSins)

# ���XExpriment��One sample t-test���G
str_OSins='randomise -i %s/expRmaps  -o %s/contTwottst -1  -n %d --T2'%(Path_current ,Path_current ,N_iter)
os.system(str_OSins)

# ���Ӹs�ժ�Rmaps�X�֦��@�ӡA�åB��design.mat�M�w�s��
str_OSins='fslmerge -t allRmaps '+ Path_current + '/contRmaps ' + Path_current + '/expRmaps '
os.system(str_OSins)

# �Y��ո�ƥu�O��ª���s���P���ժ̤��Two-Sample Unpaired T-test�A�ӫDTwo-Sample Paired T-test (Paired Two-Group Difference)
# �i�H�� design_ttest2 �ɮצW�� �s��A�ƥ� �s��B�ƥ� �ӫإ�design.mat�H��design.con
# design.mat�OGLM�ΨӤ��뤣�P�s�ժ��x�}�Cdesign.con�O���P�s�դ�����contrast(Ĵ�p��A >B ��A<B)
str_OSins='design_ttest2 %s/design %d %d'%(Path_current , len(list_control ),len(list_experim )) 
os.system(str_OSins)

# �����s�դ�����Two sample t-test
str_OSins='randomise -i %s/allRmaps -o %s/resultTwottst -d design.mat -t design.con --T2 -n %d'%(Path_current,Path_current  ,N_iter)
os.system(str_OSins)
