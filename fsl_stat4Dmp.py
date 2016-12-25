# coding: utf-8
import sys
import os
from glob import glob,iglob
from os.path import join
from argparse import ArgumentParser
import datetime
import subprocess
import multiprocessing as mp
import numpy as np
import math
import nibabel as nib


def safe_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except:
        pass

def safe_remove(ff):
    try:
        os.remove(ff)
    except:
        pass

def systemx(cmd, display=True):
    if display:
        print(cmd)
    subprocess.call(cmd, shell=True)


def r_to_z(rmap_ff):
    img = nib.load(rmap_ff)
    affine = img.affine
    img_data = img.get_data()
    img2=np.arctanh(img_data)
    new_image = nib.Nifti1Image(img2, affine)
    rmap_dir, rmap_f = os.path.split(rmap_ff)
    new_rmap_ff = os.path.join(rmap_dir,'z'+rmap_f)
    nib.save(new_image,new_rmap_ff)
    return new_rmap_ff

def processfile(list_control, list_experim, args, result_dir):
    print('Control datafiles:')
    for ii in range(len(list_control)):
        print('%d:%s' % (ii,list_control[ii]))
        if args.zmap:
            list_control[ii] = r_to_z(list_control[ii])

    print('Exp datafiles:')
    for ii in range(len(list_experim)):
        print('%d:%s' % (ii,list_experim[ii]))
        if args.zmap:
            list_experim[ii] = r_to_z(list_experim[ii])


    ctrl_rmap_ff = join(result_dir,'ctrlRmaps.nii.gz')
    exp_rmap_ff = join(result_dir,'expRmaps.nii.gz')
    all_rmap_ff = join(result_dir,'allRmaps.nii.gz')
    ctrl_1sample_ff = join(result_dir,'ctrl_1sample')
    exp_1sample_ff = join(result_dir,'exp_1sample')
    twosample_ff = join(result_dir,'twosample')
    design_ff = join(result_dir,'design')
    design_mat_ff = join(result_dir,'design.mat')
    design_con_ff = join(result_dir,'design.con')

    if args.tfce:
        multiple_comp = '-T'
    else:
        multiple_comp = '-x'

    # 列出control內所有的影像路徑
    if len(list_control) > 0:
        str_control = ' '.join(list_control)
        # 把所有control受試者的Rmap合併成一個四維的Rmaps
        str_OSins='fslmerge -t %s %s ' % (ctrl_rmap_ff,str_control)
        systemx(str_OSins)
        for f in list_control:
            safe_remove(f)

        # 做出control的One sample t-test結果
        str_OSins='randomise -i %s -o %s -1  -n %d --quiet %s' % \
                  (ctrl_rmap_ff, ctrl_1sample_ff, N_iter, multiple_comp)
        systemx(str_OSins)


    # 列出Expriment內所有的影像路徑
    if len(list_experim) > 0:
        str_experim = ' '.join(list_experim)
        # 把所有Expriment受試者的Rmap合併成一個四維的Rmaps
        # str_OSins='fslmerge -t '+ Path_current + '/expRmaps '+ str_experim
        str_OSins='fslmerge -t %s %s ' % (exp_rmap_ff,str_experim)
        systemx(str_OSins)
        for f in list_experim:
            safe_remove(f)
        # 做出Expriment的One sample t-test結果
        str_OSins='randomise -i %s -o %s -1  -n %d --quiet %s' % \
                  (exp_rmap_ff, exp_1sample_ff, N_iter, multiple_comp)
        systemx(str_OSins)



    if len(list_control) > 0 and len(list_experim) > 0:
        # 把兩個群組的Rmaps合併成一個，並且由design.mat決定群組
        str_OSins='fslmerge -t %s %s %s' % (all_rmap_ff,ctrl_rmap_ff,exp_rmap_ff)
        systemx(str_OSins)

        # 若兩組資料只是單純的兩群不同受試者比較Two-Sample Unpaired T-test，而非Two-Sample Paired T-test (Paired Two-Group Difference)
        # 可以用 design_ttest2 檔案名稱 群組A數目 群組B數目 來建立design.mat以及design.con
        # design.mat是GLM用來分辨不同群組的矩陣。design.con是不同群組之間的contrast(譬如說A >B 或A<B)
        str_OSins='design_ttest2 %s %d %d' % (design_ff, len(list_control),
                                              len(list_experim))
        systemx(str_OSins)

        # 執行兩群組之間的Two sample t-test
        str_OSins='randomise -i %s -o %s -d %s -t %s -n %d --quiet %s' % \
                  (all_rmap_ff, twosample_ff,design_mat_ff,
                   design_con_ff, N_iter, multiple_comp)
        systemx(str_OSins)
        safe_remove(ctrl_rmap_ff)
        safe_remove(exp_rmap_ff)
        safe_remove(all_rmap_ff)



parser = ArgumentParser()
parser.add_argument("-c", dest="control_dir", help="Path of control data (default: ctrl)",action='store',default='ctrl')
parser.add_argument("-e", dest="exp_dir", help="Path of experiement data (default: exp)",action='store',default='exp')
parser.add_argument("-n", dest="N_iter", help="Number of iteration (default: 100)",action='store',default=100,type=int)
parser.add_argument("-f", dest="Name_Rmapfile", help="File name of Rmap, Default: Rmap_beswarrest.nii",action='store',default='Rmap_beswarrest.nii')
parser.add_argument("-a", dest="allnii", help="Get all nii files, disregarding -f",action='store_true')
parser.add_argument("-z", dest="zmap", help="Fisher's r-to-z transform (default: none)",action='store_true')
parser.add_argument("-mp", dest="mp", help="multiple cpu processing (default: none)",action='store_true')
parser.add_argument("-nchc", dest="nchc", help="Run in NCHC (default: none)",action='store_true')
parser.add_argument("-tfce", dest="tfce", help="FSL TFCE (default: none)",action='store_true')
args = parser.parse_args()

#x=int(subprocess.check_output('. /etc/fsl/fsl.sh && fslnvols Rmap_beswarrest.nii',shell=True))

#Path_current='/home/tyhuang/FACEmars'
Path_current = os.getcwd()
N_iter=args.N_iter
#Name_Rmapfile='Rmap_beswarrest.nii'
result_dir = join(Path_current,datetime.datetime.now().strftime("stat%m%d_%H%M%S_") + \
                  args.Name_Rmapfile.split('.')[0] + 'N%d' % args.N_iter)
safe_mkdir(result_dir)
if args.allnii:
    # 分別讀取 Path_current下面的cont與exp資料夾內的MARS結果資料夾，直接從各資料夾中讀取名稱為 Name_Rmapfile(Rmap_beswarrest.nii)的檔案
    list_control = glob(join(args.control_dir,'*.nii'))
    list_control.extend(glob(join(args.control_dir,'*.nii.gz')))
    list_experim = glob(join(args.exp_dir,'*.nii'))
    list_experim.extend(glob(join(args.exp_dir,'*.nii.gz')))
else:
    list_control = [f for f in iglob(join(args.control_dir,'**',args.Name_Rmapfile),recursive=True)]
    list_experim = [f for f in iglob(join(args.exp_dir,'**',args.Name_Rmapfile),recursive=True)]


if args.nchc:
    nvols=int(subprocess.check_output('fslnvols %s' % list_control[0],shell=True))
else:
    nvols=int(subprocess.check_output('. /etc/fsl/fsl.sh && fslnvols %s' % list_control[0],shell=True))

print(nvols)
from os.path import dirname,basename,splitext,join
def filehead(f):
    return join(dirname(f),basename(f).split('.')[0])


#processfile(list_control, list_experim, args, result_dir)
if nvols == 1:
    #3D simple
    processfile(list_control, list_experim, args, result_dir)
    exit()
else:
    for ii in range(nvols):

        list_control_new=[]
        list_experim_new=[]
        for kk, f in enumerate(list_control):
            extractedfile = join(result_dir,'anatemp5566c__%d_%d.nii.gz' % (ii,kk))
            cmd = 'fslroi %s %s %d 1' % (f, extractedfile, ii)
            systemx(cmd)
            list_control_new.append(extractedfile)
        for kk, f in enumerate(list_experim):
            extractedfile = join(result_dir,'anatemp5566e__%d_%d.nii.gz' % (ii,kk))
            cmd = 'fslroi %s %s %d 1' % (f, extractedfile, ii)
            systemx(cmd)
            list_experim_new.append(extractedfile)

        result_dir_new = join(result_dir,'rsn%d' % ii)
        safe_mkdir(result_dir_new)
        if args.mp:
            p = mp.Process(target=processfile, args=(list_control_new, list_experim_new, args, result_dir_new))
            p.start()
        else:
            processfile(list_control_new, list_experim_new, args, result_dir_new)

#systemx('rm -f %s' % join(result_dir,'anatemp5566_*'))
