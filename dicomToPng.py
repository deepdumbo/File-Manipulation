from medpy.io import load
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse
import dicom
import os
import numpy
from matplotlib import pyplot, cm
import multiprocessing
import re

# Test if a given chunk is an int
def tryint(c):
	try:
		return int(c)
	except:
		return c

# turn a string into a list of string and number chunks
def alphanum_key(s):
	return [tryint(c) for c in re.split('([0-9]+)', s)]

# sort the given list
def natural_sort(list):
	list.sort(key=alphanum_key)

def convertDCM_PNG((start,end)):
	count = start
	for filename in FullPathFilesDCM[start:end]:
		print(count)
		# On-screen, things will be displayed at 80dpi regardless of what we set here
		# This is effectively the dpi for the saved figure. We need to specify it,
		# otherwise `savefig` will pick a default dpi based on your local configuration
		dpi = 80

		i, h = load(filename)
		height, width = i.shape

		# What size does the figure need to be in inches to fit the image?
		figsize = width / float(dpi), height / float(dpi)

		# Create a figure of the right size with one axes that takes up the full figure
		fig = plt.figure(figsize=figsize)
		ax = fig.add_axes([0, 0, 1, 1])

		# Hide spines, ticks, etc.
		ax.axis('off')

		# Display the image.
		ax.imshow(i, cmap = cm.Greys_r)

		# Ensure we're displaying with square pixels and the right extent.
		# This is optional if you haven't called `plot` or anything else that might
		# change the limits/aspect.  We don't need this step in this case.
		ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)

		fig.savefig('dcm_pngs/image_ ' +str(count) + '.png', dpi=dpi, transparent=True)
		plt.show()
		count += 1

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--path", required=True,
		help="path to the input images")
	ap.add_argument("-o", "--output", required=True,
		help="output file directory")
	args = vars(ap.parse_args())

	PathDicom = args["path"]
	#PathDicom = "/media/aether/My Passport/Medical Images Data/Bones/Phalanx/phalanx1_dcm/"
	FullPathFilesDCM = []  # create an empty list
	DCMFileNames = []
	for dirName, subdirList, fileList in os.walk(PathDicom):
		natural_sort(fileList)
		for filename in fileList:
			if ".dcm" in filename.lower():  # check whether the file's DICOM
				print filename
				DCMFileNames.append(filename)
				FullPathFilesDCM.append(os.path.join(dirName,filename))

	print(len(FullPathFilesDCM))

	# data = ([0,int(len(FullPathFilesDCM)//4)], [int(len(FullPathFilesDCM)//4), int(len(FullPathFilesDCM)//2)], [int(len(FullPathFilesDCM)//2), int(3*len(FullPathFilesDCM)//4)], [int(3*len(FullPathFilesDCM)//4), int(len(FullPathFilesDCM))])

	# p = multiprocessing.Pool(4) # assuming quad core

	# p.map(convertDCM_PNG, data)


	count = 0
	for filename in FullPathFilesDCM:
		print(DCMFileNames[count])
		# On-screen, things will be displayed at 80dpi regardless of what we set here
		# This is effectively the dpi for the saved figure. We need to specify it,
		# otherwise `savefig` will pick a default dpi based on your local configuration
		dpi = 80

		try:
			print filename
			i, h = load(filename)
		except Exception as e:
			print("Exception - failed to load " + str(count))
			count += 1
			continue

		height, width = i.shape

		# What size does the figure need to be in inches to fit the image?
		figsize = width / float(dpi), height / float(dpi)

		# Create a figure of the right size with one axes that takes up the full figure
		fig = plt.figure(figsize=figsize)
		ax = fig.add_axes([0, 0, 1, 1])

		# Hide spines, ticks, etc.
		ax.axis('off')

		# Display the image.
		ax.imshow(i, cmap = cm.Greys_r)

		# Ensure we're displaying with square pixels and the right extent.
		# This is optional if you haven't called `plot` or anything else that might
		# change the limits/aspect.  We don't need this step in this case.
		ax.set(xlim=[0, width], ylim=[height, 0], aspect=1)

		output_dir = args["output"]
		output_path = PathDicom + '/' + output_dir
		if not os.path.exists(output_path):
		    os.makedirs(output_path)

		fig.savefig(output_path + '/' + DCMFileNames[count][:-4] + '.png', dpi=dpi, transparent=True)
		# plt.show()
		count += 1
