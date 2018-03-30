import os
import re
import scipy.misc as misc

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

path1 = "/media/aether/ESD-USB/S02A01"
# conv_path = path1 + "bot/"

num = 300

for dirName, subdirList, fileList in os.walk(path1):
		natural_sort(fileList)
		save_dir = "S02A01_1/"
		if not os.path.exists(path1 + save_dir):
			os.makedirs(path1 + save_dir)
		for filename in fileList:
			print(filename)
			img = misc.imread(os.path.join(dirName,filename))
			misc.imsave(path1 + save_dir + str(num) + ".dcm", img)
			num += 1
