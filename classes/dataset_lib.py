# This file provides utilities for reading and preprocessing images using OpenCV,
# intended for use in dataset preparation and image processing tasks. It includes
# functions for loading images from specified paths, applying common preprocessing
# techniques (such as resizing, normalization, and grayscale conversion), and 
# preparing the images for further analysis or model training. By centralizing image
# loading and preprocessing in one file, this setup simplifies the pipeline for 
# preparing images for a dataset.
"""
Class : ImageDatasetLoader
Purpose : A class to manage reading and preprocessing images for dataset preparation
          using OpenCV. It standardizes common image processing operations for 
          consistency across the dataset.

Methods :
  - __init__ : Initializes parameters for image loading, including desired image size and color mode.
  - load_images : Reads images from a specified directory, returning them as a list or batch.
  - preprocess_image : Applies standard preprocessing steps (e.g., resizing, normalization, grayscale conversion).
  - batch_preprocess : Processes a batch of images, preparing them for analysis or model training.
"""

# Import only the function needed
from cv2 import imread, IMREAD_COLOR, IMREAD_GRAYSCALE
from cv2 import imshow, waitKey, destroyAllWindows
from cv2 import resize, INTER_NEAREST, INTER_LINEAR, INTER_CUBIC, INTER_LANCZOS4
from enum import Enum, unique
from classes.util_lib import Size, Point, Rect # type: ignore
from os import listdir
from os.path import isfile, join
from numpy import ndarray

# Enum for color mode
class ColorMode(Enum):
    """
    Enum for different color modes for image processing.

    RGB : Red-Green-Blue color mode
    GRAYSCALE : Grayscale color mode
    """
    rgb_ = IMREAD_COLOR
    grayscale_ = IMREAD_GRAYSCALE

class ImageInterpolation(Enum):
    """
    Enum for different interpolation methods for image resizing.

    NEAREST : Nearest-neighbor interpolation
    LINEAR : Bilinear interpolation
    CUBIC : Bicubic interpolation
    LANCZOS4 : Lanczos interpolation
    """
    nearest_ = INTER_NEAREST
    linear_ = INTER_LINEAR
    cubic_ = INTER_CUBIC
    lanczos4_ = INTER_LANCZOS4

# Create a image processing class
class ImageUnit:
    def __init__(self):
        pass

    def LoadImage(self, path: str, color_mode: ColorMode):
        return imread(path, color_mode.value)
        
    def ResizeImage(self, image, size: Size, interpolation: ImageInterpolation = ImageInterpolation.linear_):
        size.ClassValidation()
        return resize(image, (size.width, size.height), interpolation=interpolation.value)

    def CropImage(self, Image, rect: Rect):
        rect.ClassValidation()
        return Image[rect.point.y:rect.point.y + rect.size.height, rect.point.x:rect.point.x + rect.size.width]

    def ShowImage(self, image, name : str = "Image"):
        imshow(name, image)
        waitKey(0)
        destroyAllWindows()


# Create a dataset loader class
class DatasetUnit:
    def __init__(self):
        self.image_unit_ : ImageUnit = ImageUnit()
        self.images_ : list[ndarray] = []
        self.images_name_ : list[str] = []

    def ClearDataset(self):
        self.images_ = []
        self.images_name_ = []

    # Read a directory and get all images in the directory
    def DirImages(self, path: str) -> list[str]:
        return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    def LoadImages(self, paths: str, color_mode: ColorMode):
        """
        Load images from a specified directory and store them in the dataset.
        Images are stored as flattened arrays for further processing.
        Images names are stored for reference.
        """
        dir_images : list[str] = self.DirImages(paths)
        if len(dir_images) == 0:
            print("No images found in the directory")
            return
        if len(self.images_) > 0:
            self.images = self.images_ + [self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]
            self.images_name_ = self.images_name_ + dir_images
        else:
            self.images_ = [self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]
            self.images_name_ = dir_images

        print(f"Loaded {len(dir_images)} images from {paths}")

    def LoadImagesResize(self, paths: str, color_mode: ColorMode, size: Size):
        """
        Load images from a specified directory, resize them to a specified size, and store them in the dataset. 
        Images are stored as flattened arrays for further processing. 
        Image names are stored for reference.
        """

        dir_images : list[str] = self.DirImages(paths)
        if len(dir_images) == 0:
            print("No images found in the directory")
            return
        if len(self.images_) > 0:
            self.images = self.images_ + [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]
            self.images_name_ = self.images_name_ + dir_images
        else:
            self.images_ = [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]
            self.images_name_ = dir_images

        print(f"Loaded {len(dir_images)} images from {paths}")