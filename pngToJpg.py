import os
from PIL import Image

def pngToJpg(directory):
    for filename in os.listdir(directory):
        im = Image.open(directory + filename)
        rgb_im = im.convert('RGB')
        rgb_im.save(outdir + filename[:-4] + '.jpg')
        print("Successfully converted file:" + filename)

outdir = '/media/aether/My Passport/Medical Images Data/Visible Human Project/head_jpg/'
directory = '/media/aether/My Passport/Medical Images Data/Visible Human Project/head/'
pngToJpg(directory)
