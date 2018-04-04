import os
from PIL import Image

def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)

    return img.point(contrast)

imageDir = '/media/aether/My Passport/Medical Images Data/VESSEL12 Lungs/VESSEL12_02_cropped/VESSEL12_02_perfect_cropped/'
saveDir = '/media/aether/My Passport/Medical Images Data/VESSEL12 Lungs/VESSEL12_02_cropped/VESSEL12_02_perfect_cropped_contrast/'
for filename in os.listdir(imageDir):
    pil_img = Image.open(imageDir + filename)
    contrast_img = change_contrast(pil_img, 200)
    print filename
    contrast_img.save(saveDir + filename, "PNG")
