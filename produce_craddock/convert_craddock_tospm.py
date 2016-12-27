import numpy as np

from nilearn.image import resample_img
for ii in range(42):
    img_in_mm_space = resample_img(r'vol%04d.nii.gz' % ii, target_affine=np.array([[  -2. ,   0. ,   0. ,  78.],
     [   0. ,   2.  ,  0., -112.],
     [   0.  ,  0. ,   2. , -50.],
     [   0.  ,  0. ,   0. ,   1.],]),interpolation='nearest',target_shape=(79, 95, 68))
    img_in_mm_space.to_filename('wcraddock%04d.nii.gz' % (ii+1))
