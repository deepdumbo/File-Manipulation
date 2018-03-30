import pexpect
import argparse

ap = argparse.ArgumentParser()
# path + first file name (only input common names)
ap.add_argument("-i", "--path", required=True,
	help="path to the input images")
ap.add_argument("-d", "--output_dir", required=True,
	help="output file directory")
ap.add_argument("-o", "--output_file", required=True,
	help="output file directory")
ap.add_argument("-s", "--start", required=True,
	help="start number")
ap.add_argument("-e", "--end", required=True,
	help="end number")
args = vars(ap.parse_args())

for i in range(int(args["start"]), int(args["end"])+1):
	#child = pexpect.spawn('med2image -i Training_Batch1/segmentation-' + str(i) + '.nii -d Training_Batch1/segmentation' + str(i) + ' -o segmentation' + str(i) + '.png -s -1')
	child = pexpect.spawn('med2image -i' + args["path"] + str(i) + '.nii -d' + args["output_dir"] + str(i) + ' -o' + args["output_file"] + str(i) + '.png -s -1')
	child.expect(pexpect.EOF, timeout=None)
	print "Finished with volume # " + str(i)
