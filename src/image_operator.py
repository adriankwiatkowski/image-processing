import numpy as np
import imageio
from skimage import transform, io, color
import matplotlib.pyplot as plt

def resize_image(image, width, height):
    resized = transform.resize(image, (height, width), mode='symmetric', preserve_range=True)
    #reshaped = resized.reshape(width, height)
    return resized

def load_image(path):
    img_read = imageio.imread(path).astype(np.uint8)
    img_in = color.convert_colorspace(img_read, 'RGB', 'HSV')
    return img_in

def save_image(path, image) -> np.uint8:
    img_converted = (color.convert_colorspace(image, 'HSV', 'RGB') * 255).astype(np.uint8)
    imageio.imsave(path, img_converted)
    return img_converted

def image_to_uint8(image) -> np.uint8:
    return (color.convert_colorspace(image, 'HSV', 'RGB') * 255).astype(np.uint8)

def show_image_plot(image):
    plt.imshow(image)
    plt.show()

print('image_operator Module loaded')