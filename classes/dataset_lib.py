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
from cv2 import imread, imshow, waitKey, destroyAllWindows, imwrite, cvtColor, resize
from enum import Enum, unique
from classes.util_lib import Size, Point, Rect # type: ignore
from classes.enum import ColorMode, ColorConversion, ImageInterpolation
from os import listdir
from os.path import isfile, join
from numpy import ndarray

# Create a image processing class
class ImageUnit:
    def LoadImage(self, path: str, color_mode: ColorMode) -> ndarray:
        """
        Load image from file.

        Args:
            path (str): Path to the image file.
            color_mode (ColorMode): Color mode of the image.

        Returns:
            ndarray: Image data.

        :example:
        >>> image_agent : ImageAgent = ImageAgent()
        >>> image : ndarray = image_agent.LoadImage("path/to/image.jpg", ColorMode.rgb
        """
        image = imread(path, color_mode.value)
        return image

    def SaveImage(self, path: str, image: ndarray) -> None:
        """
        Save image to file.

        Args:
            path (str): Path to save the image.
            image (ndarray): Image data.

        :example:
        >>> image_agent : ImageAgent = ImageAgent()
        >>> image : ndarray = image_agent.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> image_agent.SaveImage("path/to/save/image.jpg", image)
        """
        imwrite(path, image)

    def ResizeImage(self, image: ndarray, size: Size[int], interpolation: ImageInterpolation = ImageInterpolation.linear_) -> ndarray:
        """
        Resize image.

        Args:
            image (ndarray): Image data.
            size (Size): Size to resize the image.
            interpolation (int): Interpolation method.

        Returns:
            ndarray: Resized image.

        :example:
        >>> image_agent : ImageAgent = ImageAgent()
        >>> image : ndarray = image_agent.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> resized_image : ndarray = image_agent.ResizeImage(image, Size(100, 100), ImageInterpolation.nearest)
        """
        return resize(image, (size.width_, size.height_), interpolation=interpolation.value)

    def ConvertColor(self, image: ndarray, conversion: ColorConversion) -> ndarray:
        """
        Convert color of image.

        Args:
            image (ndarray): Image data.
            conversion (ColorConversion): Color conversion method.

        Returns:
            ndarray: Image with converted color.

        :example:
        >>> image_agent : ImageAgent = ImageAgent()
        >>> image : ndarray = image_agent.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> converted_image : ndarray = image_agent.ConvertColor(image, ColorConversion.rgb2gray)
        """
        return cvtColor(image, conversion.value)

    def CropImage(self, image: ndarray, rect : Rect[int]) -> ndarray:
        """
        Crop image.

        Args:
            image (ndarray): Image data.
            rect (Rect): Rectangle to crop the image.

        Returns:
            ndarray: Cropped image.

        :example:
        >>> image_agent : ImageAgent = ImageAgent()
        >>> image : ndarray = image_agent.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> cropped_image : ndarray = image_agent.CropImage(image, Rect(0, 0, 100, 100))
        """
        return image[rect.point_.y_:rect.point_.y_+rect.size_.height_, rect.point_.x_:rect.point_.x_+rect.size_.width_]

    def ShowImage(self, image, name : str = "Image") -> None:
        imshow(name, image)
        waitKey(0)
        destroyAllWindows()


# Create a dataset loader class
class DatasetUnit:
    def __init__(self) -> None:
        self.image_unit_ : ImageUnit = ImageUnit()
        self.images_ : list[ndarray] = []
        self.images_name_ : list[str] = []

    def ClearDataset(self) -> None:
        self.images_ = []
        self.images_name_ = []

    # Read a directory and get all images in the directory
    def DirImages(self, path: str) -> list[str]:
        return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    def LoadImages(self, paths: str, color_mode: ColorMode) -> None:
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
            # self.images_ = self.images_ + [self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]
            # self.images_name_ = self.images_name_ + dir_images
            self.images_.extend([self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]) # type: ignore
            self.images_name_.extend(dir_images) # type: ignore
        else:
            self.images_ = [self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]
            self.images_name_ = dir_images

        print(f"Loaded {len(dir_images)} images from {paths}")

    def LoadImagesResize(self, paths: str, color_mode: ColorMode, size: Size) -> None:
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
            # self.images = self.images_ + [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]
            # self.images_name_ = self.images_name_ + dir_images
            self.images_.extend([self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]) # type: ignore
            self.images_name_.extend(dir_images) # type: ignore
        else:
            self.images_ = [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]
            self.images_name_ = dir_images

        print(f"Loaded {len(dir_images)} images from {paths}")