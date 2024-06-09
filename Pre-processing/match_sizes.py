import SimpleITK as sitk
import nibabel as nib #pip install nibabel, if nibabel is not already installed
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_fill_holes

######################################################################################################
# This script fixes the pseudo labels from MRI data that are registrated to the ultrasound images
# using ImFusion.
#
# The segmentations from ImFusion have different spacing and size than the ultrasound images, and often
# the segmentations goes out of the ultrasound image itself. This script contains different functions to fix that.
#
# - fix_size() matches the image size and spacing to the segmentation mask and saves it. It uses nearest neighbor
#              as interpolation method for the segmentation mask
# - crop_segmentation() crops the segmentation mask to match the ultrasound image itself and saves this.

######################################################################################################


# Match segmentation size, origin and spacing with ultrasound size, origin and spacing
def fix_size(folders_path, folder, us_image, seg):
    us_path = os.path.join(folders_path,folder, us_image)
    seg_path = os.path.join(folders_path,folder, seg)
    original_image = sitk.ReadImage(us_path)
    segmentation = sitk.ReadImage(seg_path)

    # Get the spacing, origin, and size of the original image
    original_spacing = original_image.GetSpacing()
    original_origin = original_image.GetOrigin()
    original_size = original_image.GetSize()

    # Resample the segmentation to match the original image
    resampler = sitk.ResampleImageFilter()
    resampler.SetSize(original_size)
    resampler.SetOutputSpacing(original_spacing)
    resampler.SetOutputOrigin(original_origin)
    resampler.SetOutputDirection(original_image.GetDirection())
    resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    resampled_segmentation = resampler.Execute(segmentation)

    # Save the resampled segmentation
    sitk.WriteImage(resampled_segmentation, seg_path)



# Crop segmentation masks to match ultrasound volume, and not just image volume
def crop_segmentation(folders_path, folder, us_image, seg):
    us_path = os.path.join(folders_path, folder, us_image)
    seg_path = os.path.join(folders_path, folder, seg)
    img = nib.load(us_path)
    affine = img.affine
    seg = nib.load(seg_path)
    data = img.get_fdata()
    data_seg = seg.get_fdata()
    data = data[:, :, :, 0]

    threshold_value = 0
    binary_mask = data > threshold_value
    binary_filled = binary_fill_holes(binary_mask).astype(int)

    data_seg[binary_filled == False] = 0
    print("Test")
    new_seg_img = nib.Nifti1Image(data_seg.astype(np.uint8), affine=affine)
    nib.save(new_seg_img, seg_path)

#crop_segmentation(folderpath, folder, us_image, seg_image)


