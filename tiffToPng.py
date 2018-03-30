import os
from PIL import Image
import re
from cv2 import imread, imwrite

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

yourpath = '/media/aether/My Passport/Medical Images Data/Kaggle Finding and Measuring Lungs in CT Data/2d_masks'
for root, dirs, files in os.walk(yourpath, topdown=False):
    natural_sort(files)
    # print files
    for name in files:
        outfile = yourpath + "_png"
        if not os.path.exists(outfile):
            os.makedirs(outfile)
        try:
            # im = Image.open(os.path.join(root, name))
            im = imread(os.path.join(root, name))
            print "Generating png for %s" % name
            print im.shape
            # im.thumbnail(im.size)
            # im.save(outfile + '/' + name[:-4] + ".png", "PNG")
            imwrite(outfile + "/" + name[:-4] + ".png", im)
        except Exception, e:
            print e
