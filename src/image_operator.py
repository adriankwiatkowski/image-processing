import numpy as np
import matplotlib.pyplot as plt
import skimage.feature
from skimage import io, color, filters

def resize_image(image, width, height):
    resized = skimage.transform.resize(image, (height, width), mode='symmetric', preserve_range=True)
    return resized

def load_image(path):
    img_read = skimage.io.imread(path)[:,:,:3]
    #img_read = skimage.io.imread(path).astype(np.uint8)
    #img_in = color.convert_colorspace(img_read, 'RGB', 'HSV')
    img_in = skimage.color.rgb2hsv(img_read)
    return img_in

def save_image(path, image) -> np.uint8:
    img_converted = _to_rgb(image)
    skimage.io.imsave(path, img_converted)
    return img_converted

def image_to_uint8(image) -> np.uint8:
    return (color.convert_colorspace(image, 'HSV', 'RGB') * 255).astype(np.uint8)

def show_image_plot(image):
    plt.imshow(image)
    plt.show()

def treshold_high_image(image, treshold):
    image[image < treshold] = 0
    return image

def treshold_low_image(image, treshold):
    image[image > treshold] = 0.25
    return image

def rgb_image(image, rgb_multiplier):
    return image * rgb_multiplier * 1.51

def _to_rgb(image):
    return (color.convert_colorspace(image, 'HSV', 'RGB') * 255).astype(np.uint8)

print('image_operator Module loaded')