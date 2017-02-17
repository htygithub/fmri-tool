import nilearn

for kk in range(1,43):
    image_wcraddock = nilearn.image.load_img(r'C:\expdata\ABIDE_bgs_stat1124\wcraddock%04d.nii.gz' % kk).get_data().astype(int)
    yy = np.bincount(image_wcraddock.flatten())
    th = np.median(yy)

    image = nilearn.image.load_img(r'C:\expdata\ABIDE_bgs_stat1124\t1_42\t1_vol%04d.nii.gz' % kk).get_data().astype(int)
    y = np.bincount(image.flatten())
    y[0] = 0
    index=y.argsort()[::-1]
    yy= y[index]

    selected_index = []
    area =[]
    area_craddock=[]
    for ii in index[:-1]:
        base = (image_wcraddock == ii)
        temp = (image == ii)
        ratio = np.sum(base & temp)/np.sum(base)
        if ratio > 0.7:
            selected_index.append(ii)
            area.append(np.sum(base & temp))
        area_craddock.append(np.sum(base))

    print(selected_index)
    print(np.sum(np.array(area)))
    print(np.sum(image>0))
