import rawpy
import imageio

path = '/home/aether/Downloads/'
imgPath = path + 'pd_icbm_normal_1mm_pn3_rf20.rawb'
raw = rawpy.imread(path)
rgb = raw.postprocess()
imageio.imsave(imgPath[:-5] + ".tiff", rgb)
