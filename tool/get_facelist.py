ctrl='''ctrl/tyhuang_pymars_face45_9284_4163/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face2_9246_f957/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face33_9275_3906/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face23_9264_9959/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face48_9285_89d9/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face4_9247_78f1/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face47_9286_3f97/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face22_9265_fa1c/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face39_9276_2ec0/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face41_9280_f802/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face49_9287_6900/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face43_9281_8a46/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face32_9274_5e26/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face30_9272_7e8f/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face31_9273_6653/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face44_9282_7fca/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face34_9277_5dab/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face38_9278_060e/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face46_9283_60cc/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face28_9271_bdc5/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face16_9259_a53f/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face40_9279_8080/RSN10/rsn10_drzstat.nii.gz
ctrl/tyhuang_pymars_face8_9250_b814/RSN10/rsn10_drzstat.nii.gz'''
exp = '''exp/tyhuang_pymars_face17_9260_d21a/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face5_9248_6233/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face21_9263_536a/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face11_9253_5d93/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face18_9258_9932/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face14_9256_c193/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face19_9261_3c20/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face29_9270_20fc/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face24_9266_1977/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face15_9257_0afb/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face7_9249_da2b/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face20_9262_498c/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face12_9254_5b34/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face10_9251_4fc3/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face26_9268_6427/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face27_9269_ab9a/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face13_9255_7847/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face9_9252_04ec/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face6_9244_a86c/RSN10/rsn10_drzstat.nii.gz
exp/tyhuang_pymars_face25_9267_2c32/RSN10/rsn10_drzstat.nii.gz'''
with open((r"list.csv"), "a") as myfile:
    myfile.writelines([ii.split('_')[2]+'\n' for ii in ctrl.split('\n') ])
    myfile.writelines([ii.split('_')[2]+'\n' for ii in exp.split('\n') ])
