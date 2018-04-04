import argparse
from PIL import Image
import cv2
import numpy
import ast
import os

def main():

	parser = argparse.ArgumentParser()

	# parser.add_argument(
	# 	"--image",
	# 	default=None,
	# 	help="file path to image. usage: --image [file_path]",
	# 	required=True
	# )
	parser.add_argument(
		"--directory",
		default=None,
		help="file path to directory conataining CT Scans. usage: --directory [file_path]",
		required=True
	)
	parser.add_argument(
		"--colors",
		default=3,
	)


	args = parser.parse_args()

	# change this if you increase materials
	colors_to_use = [[255, 0 , 0], [0, 0, 255], [0, 255, 0]]
	os.chdir(args.directory)
	for filename in os.listdir('.'):
		createImagesFromCT(filename, args.colors, colors_to_use)

def createImagesFromCT(file_path, numofcolors, colors_to_use):
	print file_path
	img = cv2.imread(file_path)
	imageheight = img.shape[0]
	imagewidth = img.shape[1]

	mask = getMask(img, imageheight, imagewidth)

	img = applyPurpleMask(img)
	mask = cv2.imwrite('mask.png', mask)


	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = Image.fromarray(img)
	img = img.convert('P', palette=Image.ADAPTIVE, colors=int(numofcolors)+1)

	tmpconfig = list(img.convert('RGB').getcolors())
	colorconfig = []

	for color in tmpconfig:
		colorconfig.append(list(color[1]))

	colorconfig.remove([128, 1, 129])

	print colorconfig

	layer_images = topColors(file_path, colorconfig, mask, colors_to_use)

	name = file_path.rsplit('.')[0]
	image_file_list = []
	count = 0
	for i in range(0, len(layer_images)):
		pil_layer = Image.fromarray(numpy.uint8(layer_images[i]))
		save_path = '/media/aether/My Passport/Medical Images Data/VESSEL12 Lungs/VESSEL12_02_cropped/VESSEL12_02_color_segment/'
		pil_layer.save(save_path + name + '_' + str(count) + '.png')
		image_file_list.append(name + '_' + str(count) + '.png')
		count += 1


def topColors(file_path, quantizedcolors, mask, colors_to_use):

	image = cv2.imread(file_path)
	height,width = image.shape[:2]
	imagewidth = image.shape[1]
	imageheight = image.shape[0]

	quantizedpalette = []

	for quantizedcolor in quantizedcolors:
		quantizedpalette = quantizedpalette + quantizedcolor

	newpixels = quantizeImage(file_path, quantizedcolors, quantizedpalette)

	original_name = file_path.rsplit('.')[0]

	layer_images = []

	for count in range(0, len(quantizedcolors)):
		createImages(newpixels.get(str(count)), quantizedcolors[count], imageheight, imagewidth, 1, mask, layer_images, colors_to_use[count])

	return layer_images

def applyPurpleMask(img):

	r = 0
	g = 1
	b = 2

	rows, cols = numpy.where((img[:,:,r] == 0) & (img[:,:,g] == 0) & (img[:,:,b] == 0))

	for x in range(0, len(rows)):
		img.itemset((rows[x], cols[x], 0), 129)
		img.itemset((rows[x], cols[x], 1), 1)
		img.itemset((rows[x], cols[x], 2), 128)

	return img

def getMask(img, imageheight, imagewidth):

	r = 0
	g = 1
	b = 2

	rows, cols = numpy.where((img[:,:,r] > 0) | (img[:,:,g] > 0) | (img[:,:,b] > 0))

	mask = numpy.zeros((imageheight, imagewidth, 3), numpy.uint8)

	for x in range(0, len(rows)):
		mask.itemset((rows[x], cols[x], 0), 255)
		mask.itemset((rows[x], cols[x], 1), 255)
		mask.itemset((rows[x], cols[x], 2), 255)

	return mask

def quantizeImage(file_path, quantizedcolors, quantizedpalette):

	quantizedpalette = quantizedpalette * 256
	quantizedpalette = quantizedpalette[0:768]
	paletteimage = Image.new('P', (16, 16))
	paletteimage.putpalette(quantizedpalette)
	image = Image.open(file_path)

	adaptedimage = quantizetopalette(image, paletteimage, dither=False)
	adaptedimage = numpy.array(adaptedimage.convert('RGBA'))

	newpixels = {}
	key = 0

	for quantizedcolor in quantizedcolors:
		r = 0
		g = 1
		b = 2
		rows, cols = numpy.where((adaptedimage[:,:,r] == quantizedcolor[0]) & (adaptedimage[:,:,g] == quantizedcolor[1]) & (adaptedimage[:,:,b] == quantizedcolor[2]))
		coordinates = []

		for i in range(0, len(rows)):
			coordinates.append(str([rows[i], cols[i]]))

		newpixels[str(key)] = coordinates
		key += 1

	return newpixels

def quantizetopalette(silf, palette, dither=False):
	silf.load()
	palette.load()

	if palette.mode != "P":
	    raise ValueError("bad mode for palette image")
	if silf.mode != "RGB" and silf.mode != "L":
		raise ValueError(
			"only RGB or L mode images can be quantized to a palette"
			)
	im = silf.im.convert("P", 1 if dither else 0, palette.im)

	try:
		return silf._new(im)
	except AttributeError:
		return silf._makeself(im)

def createImages(coordinates, color, imageheight, imagewidth, backgroundflag, mask, layer_images, colors_to_use):

	blank_image = numpy.zeros((imageheight, imagewidth, 3), numpy.uint8)

	if int(backgroundflag) == 1:
		r = 0
		g = 1
		b = 2

		boundary = cv2.imread('mask.png', 0)
		rows, cols = numpy.where(boundary > 0)
		maskcoordinates = []

		for i in range(0, len(rows)):
			maskcoordinates.append(str([rows[i], cols[i]]))

		setofcoords = set(coordinates)
		setofmask = set(maskcoordinates)
		superset = setofmask.intersection(setofcoords)

		for obj in superset:
			coord = ast.literal_eval(obj)
			blank_image.itemset((coord[0], coord[1], 0), colors_to_use[0])
			blank_image.itemset((coord[0], coord[1], 1), colors_to_use[1])
			blank_image.itemset((coord[0], coord[1], 2), colors_to_use[2])
		for y in range(0, imageheight):
			blank_image.itemset((y, 0, 0), colors_to_use[0])
			blank_image.itemset((y, 0, 1), colors_to_use[1])
			blank_image.itemset((y, 0, 2), colors_to_use[2])
			blank_image.itemset((y, imagewidth-1, 0), colors_to_use[0])
			blank_image.itemset((y, imagewidth-1, 1), colors_to_use[1])
			blank_image.itemset((y, imagewidth-1, 2), colors_to_use[2])
		for x in range(0, imagewidth):
			blank_image.itemset((0, x, 0), colors_to_use[0])
			blank_image.itemset((0, x, 1), colors_to_use[1])
			blank_image.itemset((0, x, 2), colors_to_use[2])
			blank_image.itemset((imageheight-1, x, 0), colors_to_use[0])
			blank_image.itemset((imageheight-1, x, 1), colors_to_use[1])
			blank_image.itemset((imageheight-1, x, 2), colors_to_use[2])
		layer_images.append(blank_image)
	else:
		for obj in coordinates:
			coord = ast.literal_eval(obj)
			blank_image.itemset((coord[0], coord[1], 0), colors_to_use[0])
			blank_image.itemset((coord[0], coord[1], 1), colors_to_use[1])
			blank_image.itemset((coord[0], coord[1], 2), colors_to_use[2])
		for y in range(0, imageheight):
			blank_image.itemset((y, 0, 0), colors_to_use[0])
			blank_image.itemset((y, 0, 1), colors_to_use[1])
			blank_image.itemset((y, 0, 2), colors_to_use[2])
			blank_image.itemset((y, imagewidth-1, 0), colors_to_use[0])
			blank_image.itemset((y, imagewidth-1, 1), colors_to_use[1])
			blank_image.itemset((y, imagewidth-1, 2), colors_to_use[2])
		for x in range(0, imagewidth):
			blank_image.itemset((0, x, 0), colors_to_use[0])
			blank_image.itemset((0, x, 1), colors_to_use[1])
			blank_image.itemset((0, x, 2), colors_to_use[2])
			blank_image.itemset((imageheight-1, x, 0), colors_to_use[0])
			blank_image.itemset((imageheight-1, x, 1), colors_to_use[1])
			blank_image.itemset((imageheight-1, x, 2), colors_to_use[2])
		layer_images.append(blank_image)

main()
