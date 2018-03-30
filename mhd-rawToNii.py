import skimage.io as skio
import vtk
import vtkInterface
from vtk.util import numpy_support
import numpy as np
import SimpleITK
import matplotlib.pyplot as plt
import pexpect

path = '/media/aether/My Passport/Medical Images Data/VESSEL12 Lungs/VESSEL12_images/'

path = path + 'VESSEL12_20/'
im_filename = 'VESSEL12_20.mhd'
im_filepath = path + im_filename
# img = skio.imread(filepath, plugin='simpleitk')
# # img = np.reshape(img, (img.shape[1],img.shape[2],img.shape[0]))
# print img.shape

# plt.imshow(img[60],cmap='gray')
# plt.show()

# convert file to .nii
img = SimpleITK.ReadImage(im_filepath)
new_im_filename = im_filename[:-4] + ".nii"
SimpleITK.WriteImage(img, path + new_im_filename)
#
# gt_filename = "gt_binary.mhd"
# gt_filepath = path + gt_filename
# gt_img = SimpleITK.ReadImage(gt_filepath)
# new_gt_filename = gt_filename[:-4] + ".nii"
# SimpleITK.WriteImage(gt_img, path + new_gt_filename)


# png_directory_name = "image_png"
# png_file_name = "image.png"
# # use med2image to convert .nii to pngs
# child = pexpect.spawn('med2image -i' + path + new_filename + '-d' + path + png_directory_name + '-o' + path + png_file_name)
# child.expect(pexpect.EOF, timeout=None)


# VTK_data = numpy_support.numpy_to_vtk(num_array=img.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
# print type(VTK_data)
# mesh = vtk.vtkImageData()
# mesh.SetDimensions(img.shape)
# mesh.GetPointData().SetScalars(VTK_data)
# mesh.Plot(color='orange')
