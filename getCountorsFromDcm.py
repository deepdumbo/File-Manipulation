import dicom

filepath = '/media/aether/My Passport/Medical Images Data/LCTSC - Lung CT Segmentation Challenge 2017/train/LCTSC-Train-S1-001/S1-001_countors/'

ds = dicom.read_file(filepath + "000000.dcm", force=True)
# print ds.dir("contour")
ctrs = ds.ROIContourSequence
# print len(ctrs) #5
# print len(ctrs[0]) #3

print ctrs[0].ContourSequence[0].ContourData

# ss = dicom.read_file('rtss.dcm')
# ss.ROIContours[0].Contours[0].ContourData 
