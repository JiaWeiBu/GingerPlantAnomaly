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
from os import listdir, makedirs
from os.path import isfile, join, exists, dirname
from cv2 import imread, imshow, waitKey, destroyAllWindows, imwrite, cvtColor, resize
from numpy import ndarray

from classes.util_lib import Size, Rect # type: ignore
from classes.enum import ColorMode, ColorConversion, ImageInterpolation

# Create a image processing class
class ImageUnit:
    """
    Agent for image operations.
    Used for loading, saving, resizing, converting color, and cropping images.

    Attributes:
        None

    Methods:
        LoadImage: Load image from file.
        SaveImage: Save image to file.
        ResizeImage: Resize image.
        ConvertColor: Convert color of image.
        CropImage: Crop image.
        LoadVideo: Load video from file.
        FindPlantMask: Find plant mask in the image using color range.
        FindPlantContour: Find plant contour in the mask.

    :example:
    >>> image_unit : ImageUnit = ImageUnit()  
    >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
    """

    def __init__(self):
        ...
    
    def LoadImage(self, path: str, color_mode: ColorMode) -> ndarray:
        """
        Load image from file.

        Args:
            path (str): Path to the image file.
            color_mode (ColorMode): Color mode of the image.

        Returns:
            ndarray: Image data.

        :example:
        >>> image_unit : ImageUnit = ImageUnit()
        >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
        """
        assert exists(dirname(path)), f"{dirname(path)} not found"

        image : ndarray = imread(path, color_mode.value)
        return image

    def SaveImage(self, path: str, image: ndarray) -> None:
        """
        Save image to file.

        Args:
            path (str): Path to save the image.
            image (ndarray): Image data.

        :example:
        >>> image_unit : ImageUnit = ImageUnit()
        >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> image_unit.SaveImage("path/to/save/image.jpg", image)
        """
        assert path.endswith((".jpg", ".png")), "Invalid file format"

        # Ensure the directory exists
        directory = dirname(path)
        if not exists(directory):
            makedirs(directory)

        # Save the image
        if not imwrite(path, image):
            raise IOError(f"Failed to save image to {path}")

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
        >>> image_unit : ImageUnit = ImageUnit()
        >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> resized_image : ndarray = image_unit.ResizeImage(image, Size(100, 100), ImageInterpolation.linear)
        """
        assert size.width_ > 0 and size.height_ > 0, "Invalid size"

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
        >>> image_unit : ImageUnit = ImageUnit()
        >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> converted_image : ndarray = image_unit.ConvertColor(image, ColorConversion.rgb2gray)
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
        >>> image_unit : ImageUnit = ImageUnit()
        >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> cropped_image : ndarray = image_unit.CropImage(image, Rect(Point(0, 0), Size(100, 100)))
        """
        assert rect.point_.x_ >= 0 and rect.point_.y_ >= 0, "Invalid rectangle point"
        assert rect.size_.width_ > 0 and rect.size_.height_ > 0, "Invalid rectangle size"

        return image[rect.point_.y_:rect.point_.y_+rect.size_.height_, rect.point_.x_:rect.point_.x_+rect.size_.width_]
    
    def ShowImage(self, image, name : str = "Image") -> None:
        """
        Display image.

        Args:
            image (ndarray): Image data.
            name (str): Name of the window.

        :example:
        >>> image_unit : ImageUnit = ImageUnit()
        >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
        >>> image_unit.ShowImage(image, "Image")
        """
        imshow(name, image)
        waitKey(0)
        destroyAllWindows()


# Create a dataset loader class
class DatasetUnit:
    """
    Agent for dataset operations.
    Such as loading images and process, it uses imageunit as most of the functionality is related to image processing.

    Attributes:
        image_unit_ : ImageUnit : Image processing unit.
        images_ : list[ndarray] : List of images.
        images_name_ : list[str] : List of image names.
    
    Methods:
        ClearDataset: Clear the dataset.
        DirImages: Read a directory and get all images in the directory.
        LoadImages: Load images from a specified directory and store them in the
                    dataset. Images are stored as flattened arrays for further processing.
                    Images names are stored for reference.
        LoadImagesResize: Load images from a specified directory, resize them to a specified size,
                          and store them in the dataset. Images are stored as flattened arrays for further processing.
                          Image names are stored for reference.

    :example:
    >>> dataset_unit : DatasetUnit = DatasetUnit()
    >>> dataset_unit.LoadImages("path/to/images", ColorMode.rgb)
    """

    def __init__(self) -> None:
        """
        Initialize the dataset unit.
        """
        self.image_unit_ : ImageUnit = ImageUnit()
        self.images_ : list[ndarray] = []
        self.images_name_ : list[str] = []

    def ClearDataset(self) -> None:
        """
        Clear the dataset.

        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.ClearDataset()
        """
        self.images_ = []
        self.images_name_ = []

    # Read a directory and get all images in the directory
    def DirImages(self, path: str) -> list[str]:
        """
        Read a directory and get all images in the directory.

        Args:
            path (str): Path to the directory.
        
        Returns:
            list[str]: List of image paths.
        
        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.DirImages("path/to/images")
        """
        return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    def LoadImages(self, paths: str, color_mode: ColorMode) -> None:
        """
        Load images from a specified directory and store them in the dataset.
        Images are stored as flattened arrays for further processing.
        Images names are stored for reference.

        Args:
            paths (str): Path to the directory.
            color_mode (ColorMode): Color mode of the images.
        
        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.LoadImages("path/to/images", ColorMode.rgb)
        """
        dir_images : list[str] = self.DirImages(paths)
        if len(dir_images) == 0:
            print("No images found in the directory")
            return
        if len(self.images_) > 0:
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

        Args:
            paths (str): Path to the directory.
            color_mode (ColorMode): Color mode of the images.
            size (Size): Size to resize the images.
        
        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.LoadImagesResize("path/to/images", ColorMode.rgb, Size(100, 100))
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