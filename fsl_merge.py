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
from os.path import dirname,basename,splitext,join
#def filehead(f):
#    return join(dirname(f),basename(f).split('.')[0])


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

    for ii in range(len(list_control)):
        #print('%d:%s' % (ii,list_control[ii]))
        if args.zmap:
            list_control[ii] = r_to_z(list_control[ii])

    #print('Exp datafiles:')
    for ii in range(len(list_experim)):
        #print('%d:%s' % (ii,list_experim[ii]))
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



parser = ArgumentParser()
arser.add_argument("-f", dest="Name_Rmapfile", help="File name of Rmap, Default: Rmap_beswarrest.nii",action='store',default='Rmap_beswarrest.nii')
parser.add_argument("-l", dest="ctrl_txt", help="Path of data ",action='store',default='none')
args = parser.parse_args()

#x=int(subprocess.check_output('. /etc/fsl/fsl.sh && fslnvols Rmap_beswarrest.nii',shell=True))

#Path_current='/home/tyhuang/FACEmars'
Path_current = os.getcwd()
N_iter=args.N_iter
#Name_Rmapfile='Rmap_beswarrest.nii'
result_dir = join(Path_current,datetime.datetime.now().strftime("mergedata_S%m%d_%H%M%S_") + \
                  args.Name_Rmapfile.split('.')[0])

if args.ctrl_txt is not 'none':
    with open(args.ctrl_txt, 'r') as f:
        list_control_dirs = [line.strip() for line in f]
    list_control = []
    for dd in list_control_dirs:
        list_control.extend(iglob(join(dd,'**',args.Name_Rmapfile),recursive=True))


print(list_control)
if args.nchc:
    nvols=int(subprocess.check_output('fslnvols %s' % list_control[0],shell=True))
else:
    nvols=int(subprocess.check_output('. /etc/fsl/fsl.sh && fslnvols %s' % list_control[0],shell=True))


with open(join(result_dir,"processlog.txt"), "a") as myfile:
    myfile.write("\nCotrol files:\n")
    myfile.write('\n'.join(list_control))
    myfile.write("\nEXP files:\n")
    myfile.write('\n'.join(list_experim))

#processfile(list_control, list_experim, args, result_dir)
if nvols == 1:
    #3D simple
    processfile(list_control, list_experim, args, result_dir)
    exit()
else:
    for ii in list(range(nvols)):

        list_control_new=[]
        for kk, f in enumerate(list_control):
            extractedfile = join(result_dir,'anatemp5566c__%d_%d.nii.gz' % (ii,kk))
            cmd = 'fslroi %s %s %d 1' % (f, extractedfile, ii)
            systemx(cmd)
            list_control_new.append(extractedfile)

        result_dir_new = join(result_dir,'rsn%d' % ii)
        safe_mkdir(result_dir_new)
        processfile(list_control_new, list_experim_new, args, result_dir_new)
