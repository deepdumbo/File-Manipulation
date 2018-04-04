import os

current_folder = '/media/aether/My Passport/Medical Images Data/VESSEL12 Lungs/VESSEL12_02_cropped/VESSEL12_02_perfect_cropped/'
destination = '/media/aether/My Passport/Medical Images Data/VESSEL12 Lungs/VESSEL12_02_cropped/green_lung/'

for filename in os.listdir(current_folder):
    if '_2' in filename:
        print "Moving " + filename
        os.rename(current_folder + filename, destination + filename)
