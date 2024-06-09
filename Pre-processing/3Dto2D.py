import os
import nibabel as nib
import numpy as np
from glob import glob

########################################################################################################
# This code is used to slice the 3D images in 2D slices in all 3 directions.
# This requires that the 3D ultrasound image and the segmentation image has the same dimention, spacing,
# origin and affine.

# Since the folder structure and the images are a bit different for the different datasets, there is one
# code for each dataset.

# The code gives the 2D slices a new name and folder structure that matches nnU-Net. The ultrasound images are
# placed in a folder "imageTr" with name: BT_US_2D_XXXXXXXX_0000.nii.gz.
# The labels are stored in "labelsTr" with name: BT_US_2D_XXXXXXXX.nii.gz. XXXXXXXX gives the images an
# unique number that is filled with zeros in front to create a 8-digit long number for each.

# The first digit of the unique number shows where the images are from. If it starts with:
# - 0 it is from ReMIND
# - 1 it is from HUNT Cloud
# - 2 it is from RESECT
# - 3 it is from the test set of CuRIOUS-SEG

# The code also writes the old image name and the last slice's unique number in each slice direction to a file.

# Example:
#   ReMIND-071_US_post, x, 725, y, 1319, z, 1469
#   ReMIND-071_US_pre, x, 2223, y, 2838, z, 2967
#
# This means that the slices from the 3D image ReMIND-071_US_pre got slices in the x-direction with unique numbers
# from 1470 to 2223, and from 2224 to 2838 in the y-direction and 2839 to 2967 in the z-direction.
########################################################################################################

# For ReMIND
def ReMIND_3Dto2D(folders_path):
    # file to store information about from which 3D image the slices come from.
    fw = open("3Dto2D_ReMIND_z_direction.txt", "a")
    # path to where the slices should be saved.
    new_path = "/Users/mathildegajdafaanes/Documents/Master/Data/ReMIND/ReMIND_2D_z"
    # collecting all ReMIND-XXX folders from the ReMIND folder.
    main_folder = [f for f in os.listdir(folders_path) if not f.startswith('.')]
    # to give the unique number to each slice
    teller = 0
    new_name = "BT_US_2D_"
    # going through every ReMIND-XXX folder in the ReMIND folder
    for folder in main_folder:
        # collecting only ultrasound images
        files = [f for f in os.listdir(os.path.join(folders_path, folder)) if not f.startswith('.')]
        us_imgs = [f for f in files if "US" in f and not "seg" in f]
        # going through all ultrasound images
        for us_img in us_imgs:
            img_file = os.path.join(folders_path, folder, us_img)
            seg_file = os.path.join(folders_path, folder, us_img[:-7] + "_seg.nii.gz")
            name = us_img[:-7]
            print(name)
            if os.path.isfile(seg_file):
                img = nib.load(img_file)
                seg = nib.load(seg_file)
                affine = img.affine
                # the ReMIND dataset has shape (x,y,z,1), so to get it to (x,y,z)
                data = img.get_fdata()
                data = data[:, :, :, 0]
                data_seg = seg.get_fdata()
                print(np.max(data_seg))
                # some labels had 0 and 255 as values so this is for getting everything as 0s and 1s
                data_seg[data_seg > 0] = 1
                x_dim, y_dim, z_dim = data.shape
                print(x_dim, y_dim, z_dim)

                # going through every slice in x-direction and saving image and segmentation
                for i in range(x_dim):
                    teller += 1
                    slice = data[i, :, :]
                    slice_seg = data_seg[i, :, :]
                    print(i)
                    slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                    slice_img_path = new_path + "/imagesTr/" + new_name + str(teller).zfill(8) + "_0000.nii.gz"
                    slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                    slice_seg_path = new_path + "/labelsTr/" + new_name + str(teller).zfill(8) + ".nii.gz"
                    nib.save(slice_img, slice_img_path)
                    nib.save(slice_seg_img, slice_seg_path)
                antall_hver_3Dx = teller

                # going through every slice in y-direction and saving image and segmentation
                for i in range(y_dim):
                    teller += 1
                    slice = data[:, i, :]
                    slice_seg = data_seg[:, i, :]
                    print(i)
                    slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                    slice_img_path = new_path + "/imagesTr/" + new_name + str(teller).zfill(8) + "_0000.nii.gz"
                    slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                    slice_seg_path = new_path + "/labelsTr/" + new_name + str(teller).zfill(8) + ".nii.gz"
                    nib.save(slice_img, slice_img_path)
                    nib.save(slice_seg_img, slice_seg_path)
                antall_hver_3Dy = teller

                # going through every slice in z-direction and saving image and segmentation
                for i in range(z_dim):
                    teller += 1
                    slice = data[:, :, i]
                    slice_seg = data_seg[:, :, i]
                    print(i)
                    slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                    slice_img_path = new_path + "/imagesTr/" + new_name + str(teller).zfill(8) + "_0000.nii.gz"
                    slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                    slice_seg_path = new_path + "/labelsTr/" + new_name + str(teller).zfill(8) + ".nii.gz"
                    nib.save(slice_img, slice_img_path)
                    nib.save(slice_seg_img, slice_seg_path)
                antall_hver_3Dz = teller

                # writing name-information to file
                fw.write(name + ", x, " + str(antall_hver_3Dx) + ", y, " + str(antall_hver_3Dy) + ", z, " + str(antall_hver_3Dz) + "\n")
                #fw.write(name + ", z, " + str(antall_hver_3Dz) + "\n")
    fw.close()


# path to ReMIND folder
folders_path = "/Users/mathildegajdafaanes/Documents/Master/Data/ReMIND/ReMIND_with_MRI_pseudolabels"
#ReMIND_3Dto2D(folders_path)



def HC_3Dto2D(folders_path):
    fw = open("3Dto2D_all_info_HC.txt", "a")
    main_folder = [f for f in os.listdir(folders_path) if not f.startswith('.')]
    new_path = ""
    teller = 10000000
    for folder in main_folder:
        # Collecting ultrasound image and corresponding segmentation image
        files = [f for f in os.listdir(os.path.join(folders_path, folder)) if not f.startswith('.')]
        us_imgs = [f for f in files if "US" in f and not "seg" in f]
        for us_img in us_imgs:
            img_file = os.path.join(folders_path, folder, us_img)
            seg_file = os.path.join(folders_path, folder, us_img[:-8] + "seg_" + us_img[-8:])
            name = us_img[:-7]
            new_name = "BT_US_2D_"
            print(name)
            print(us_img[:-8] + "seg_" + us_img[-8:])
            if os.path.isfile(seg_file):
                img = nib.load(img_file)
                seg = nib.load(seg_file)
                print(img.header.get_zooms())
                print(seg.header.get_zooms())
                affine = img.affine
                data = img.get_fdata()
                data_seg = seg.get_fdata()
                x_dim, y_dim, z_dim = data.shape
                print(x_dim, y_dim, z_dim)


                for i in range(x_dim):
                    teller += 1
                    slice = data[i, :, :]
                    slice_seg = data_seg[i, :, :]
                    print(i)
                    slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                    slice_img_path = new_path + "/imagesTr/" + new_name + str(teller).zfill(8) + "_0000.nii.gz"
                    slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                    slice_seg_path = new_path + "/labelsTr/" + new_name + str(teller).zfill(8) + ".nii.gz"
                    nib.save(slice_img, slice_img_path)
                    nib.save(slice_seg_img, slice_seg_path)
                antall_hver_3Dx = teller
                for i in range(y_dim):
                    teller += 1
                    slice = data[:, i, :]
                    slice_seg = data_seg[:, i, :]
                    print(i)
                    slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                    slice_img_path = new_path + "/imagesTr/" + new_name + str(teller).zfill(8) + "_0000.nii.gz"
                    slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                    slice_seg_path = new_path + "/labelsTr/" + new_name + str(teller).zfill(8) + ".nii.gz"
                    nib.save(slice_img, slice_img_path)
                    nib.save(slice_seg_img, slice_seg_path)
                antall_hver_3Dy = teller

                for i in range(z_dim):
                    teller += 1
                    slice = data[:, :, i]
                    slice_seg = data_seg[:, :, i]
                    print(i)
                    slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                    slice_img_path = new_path + "/imagesTr/" + new_name + str(teller).zfill(8) + "_0000.nii.gz"
                    slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                    slice_seg_path = new_path + "/labelsTr/" + new_name + str(teller).zfill(8) + ".nii.gz"
                    nib.save(slice_img, slice_img_path)
                    nib.save(slice_seg_img, slice_seg_path)
                antall_hver_3Dz = teller
                #fw.write(name + ", " + str(antall_hver_3Dz) + "\n")
                fw.write(name + ", x," + str(antall_hver_3Dx) + ", y," + str(antall_hver_3Dy)+ ", z," +str(antall_hver_3Dz)+ "\n")
    fw.close()



folder = " "
#HC_3Dto2D(folder)


########################################################################################################
# for RESECT and the test set of CuRIOUS-SEG
def RESECT_and_testset_3Dto2D():
    f = open("RESECT_3Dto2D_info.txt", "a")
    baseDir = "/Users/mathildegajdafaanes/Documents/Master/Data/RESECT/RESECT"
    new_path = "/Users/mathildegajdafaanes/Documents/Master/Data/RESECT/RESECT_2D_all_directions"
    img_files = glob(baseDir + '/imagesTr/*.nii.gz')
    teller = 20000000  # 30000000 for test set
    antall_hver_3Dx = 0
    antall_hver_3Dy = 0
    antall_hver_3Dz = 0
    for img_file in img_files:
        name = img_file[-28:-12]
        newname = "BT_US_2D_"
        print(name)
        seg_path = baseDir + "/labelsTr/" + name + ".nii.gz"  # baseDir+"/labelsTs/"+name+".nii.gz" for test set
        if os.path.exists(seg_path):
            img = nib.load(img_file)
            seg = nib.load(seg_path)
            affine = img.affine
            data = img.get_fdata()
            data_seg = seg.get_fdata()
            x_dim, y_dim, z_dim = data.shape
            print(x_dim, y_dim, z_dim)

            for i in range(x_dim):
                teller += 1
                slice = data[i, :, :]
                slice_seg = data_seg[i, :, :]
                print(i)
                slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                slice_img_path = new_path + "/imagesTs/" + newname + str(teller).zfill(8) + "_0000.nii.gz"
                slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                slice_seg_path = new_path + "/labelsTs/" + newname + str(teller).zfill(8) + ".nii.gz"
                nib.save(slice_img, slice_img_path)
                nib.save(slice_seg_img, slice_seg_path)

            antall_hver_3Dx = teller
            for i in range(y_dim):
                teller += 1
                slice = data[:, i, :]
                slice_seg = data_seg[:, i, :]
                print(i)
                slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                slice_img_path = new_path + "/imagesTs/" + newname + str(teller).zfill(8) + "_0000.nii.gz"
                slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                slice_seg_path = new_path + "/labelsTs/" + newname + str(teller).zfill(8) + ".nii.gz"
                nib.save(slice_img, slice_img_path)
                nib.save(slice_seg_img, slice_seg_path)
            antall_hver_3Dy = teller

            for i in range(z_dim):
                teller += 1
                slice = data[:, :, i]
                slice_seg = data_seg[:, :, i]
                print(i)
                slice_img = nib.Nifti1Image(slice.astype(np.uint8), affine=affine)
                slice_img_path = new_path + "/imagesTs/" + newname + str(teller).zfill(8) + "_0000.nii.gz"
                slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                slice_seg_path = new_path + "/labelsTs/" + newname + str(teller).zfill(8) + ".nii.gz"
                nib.save(slice_img, slice_img_path)
                nib.save(slice_seg_img, slice_seg_path)
            antall_hver_3Dz = teller
            # f.write(name + ", z, " + str(antall_hver_3Dz) +"\n")
            f.write(name + ", x, " + str(antall_hver_3Dx) + ", y, " + str(antall_hver_3Dy) + ", z, " + str(
                antall_hver_3Dz) + "\n")
    f.close()

# RESECT_and_testset_3Dto2D()

def testset_3Dto2D():
    f = open("reg_3Dto2D_info.txt", "a")
    baseDir = "/Users/mathildegajdafaanes/Documents/Master/Data/Test_registrering/labels_reg"
    new_path = "/Users/mathildegajdafaanes/Documents/Master/Data/Test_registrering/labels_reg_RESECT_2D_new"
    #seg_files = glob(baseDir + '/*.nii.gz')
    #files = ["BT_US_BEFORE_026.nii.gz", "BT_US_BEFORE_025.nii.gz", "BT_US_BEFORE_029.nii.gz", "BT_US_BEFORE_027.nii.gz", "BT_US_BEFORE_028.nii.gz"]
    files = ["BT_US_BEFORE_023.nii.gz","BT_US_BEFORE_011.nii.gz", "BT_US_BEFORE_004.nii.gz","BT_US_BEFORE_018.nii.gz","BT_US_BEFORE_001.nii.gz","BT_US_BEFORE_008.nii.gz","BT_US_BEFORE_014.nii.gz","BT_US_BEFORE_017.nii.gz","BT_US_BEFORE_002.nii.gz","BT_US_BEFORE_007.nii.gz","BT_US_BEFORE_012.nii.gz","BT_US_BEFORE_020.nii.gz","BT_US_BEFORE_015.nii.gz","BT_US_BEFORE_009.nii.gz","BT_US_BEFORE_019.nii.gz","BT_US_BEFORE_005.nii.gz","BT_US_BEFORE_010.nii.gz","BT_US_BEFORE_022.nii.gz","BT_US_BEFORE_021.nii.gz","BT_US_BEFORE_013.nii.gz","BT_US_BEFORE_006.nii.gz","BT_US_BEFORE_003.nii.gz","BT_US_BEFORE_016.nii.gz"]
    teller = 20000000  # 30000000 for test set
    antall_hver_3Dx = 0
    antall_hver_3Dy = 0
    antall_hver_3Dz = 0
    #print(seg_files)
    for file in files:
        seg_file = os.path.join(baseDir, file)
        print(seg_file)
        name = seg_file[-23:-7]
        newname = "/BT_US_2D_"
        print(name)
        print("hi")
        seg_path = os.path.join(baseDir, name + ".nii.gz")  # baseDir+"/labelsTs/"+name+".nii.gz" for test set
        if os.path.isfile(seg_path):
            seg = nib.load(seg_path)
            affine = seg.affine
            data = seg.get_fdata()
            data_seg = seg.get_fdata()
            x_dim, y_dim, z_dim = data.shape
            print(x_dim, y_dim, z_dim)

            for i in range(x_dim):
                teller += 1
                slice_seg = data_seg[i, :, :]
                print(i)
                slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                slice_seg_path = new_path +  newname + str(teller).zfill(8) + ".nii.gz"
                nib.save(slice_seg_img, slice_seg_path)

            antall_hver_3Dx = teller
            for i in range(y_dim):
                teller += 1
                slice_seg = data_seg[:, i, :]
                print(i)
                slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                slice_seg_path = new_path + newname + str(teller).zfill(8) + ".nii.gz"
                nib.save(slice_seg_img, slice_seg_path)
            antall_hver_3Dy = teller

            for i in range(z_dim):
                teller += 1
                slice_seg = data_seg[:, :, i]
                print(i)
                slice_seg_img = nib.Nifti1Image(slice_seg.astype(np.uint8), affine=affine)
                slice_seg_path = new_path  + newname + str(teller).zfill(8) + ".nii.gz"
                nib.save(slice_seg_img, slice_seg_path)
            antall_hver_3Dz = teller
            # f.write(name + ", z, " + str(antall_hver_3Dz) +"\n")
            f.write(name + ", x, " + str(antall_hver_3Dx) + ", y, " + str(antall_hver_3Dy) + ", z, " + str(
                antall_hver_3Dz) + "\n")
    f.close()


# testset_3Dto2D()