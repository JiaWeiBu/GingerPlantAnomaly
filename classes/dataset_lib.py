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
@unique
class ColorMode(Enum):
    """
    Enum for different color modes for image processing.

    RGB : Red-Green-Blue color mode
    GRAYSCALE : Grayscale color mode
    """
    rgb_ = IMREAD_COLOR
    grayscale_ = IMREAD_GRAYSCALE

@unique
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

@unique
class MVTecDatasetType(Enum):
    bottle_ = "bottle"
    cable_ = "cable"
    capsule_ = "capsule"
    carpet_ = "carpet"
    grid_ = "grid"
    hazelnut_ = "hazelnut"
    leather_ = "leather"
    metal_nut_ = "metal_nut"
    pill_ = "pill"
    screw_ = "screw"
    tile_ = "tile"
    toothbrush_ = "toothbrush"
    transistor_ = "transistor"
    wood_ = "wood"
    zipper_ = "zipper"

@unique
class MVTecDatasetTypeAnomaly(Enum):
    broken_large_ = "broken_large" 
    broken_small_ = "broken_small"
    contamination_ = "contamination"
    bent_wire_ = "bent_wire"
    cable_swap_ = "cable_swap"
    combined_ = "combined"
    cut_inner_insulation_ = "cut_inner_insulation"
    cut_outer_insulation_ = "cut_outer_insulation"
    missing_cable_ = "missing_cable"
    missing_wire_ = "missing_wire"
    poke_insulation_ = "poke_insulation"
    crack_ = "crack"
    faulty_imprint_ = "faulty_imprint"
    poke_ = "poke"
    scratch_ = "scratch"
    squeeze_ = "squeeze"
    color_ = "color"
    cut_ = "cut"
    hole_ = "hole"
    metal_contamination_ = "metal_contamination"
    thread_ = "thread"
    bent_ = "bent"
    broken_ = "broken"
    glue_ = "glue"
    print_ = "print"
    fold_ = "fold"
    flip_ = "flip"
    pill_type_ = "pill_type"
    manipulated_front_ = "manipulated_front"
    scratch_head_ = "scratch_head"
    scratch_neck_ = "scratch_neck"
    thread_side_ = "thread_side"
    thread_top_ = "thread_top"
    glue_strip_ = "glue_strip"
    gray_stroke_ = "gray_stroke"
    oil_ = "oil"
    rough_ = "rough"
    defective_ = "defective"
    bent_lead_ = "bent_lead"
    cut_lead_ = "cut_lead"
    damaged_case_ = "damaged_case"
    misplaced_ = "misplaced"
    liquid_ = "liquid"
    broken_teeth_ = "broken_teeth"
    fabric_border_ = "fabric_border"
    fabric_interior_ = "fabric_interior"
    split_teeth_ = "split_teeth"
    squeezed_teeth_ = "squeezed_teeth"

# hash table for MVTec dataset
MVTecDataset : dict[MVTecDatasetType, list[MVTecDatasetTypeAnomaly]] = {
    MVTecDatasetType.bottle_ : [
        MVTecDatasetTypeAnomaly.broken_large_, 
        MVTecDatasetTypeAnomaly.broken_small_, 
        MVTecDatasetTypeAnomaly.contamination_
        ],

    MVTecDatasetType.cable_ : [ 
        MVTecDatasetTypeAnomaly.bent_wire_,
        MVTecDatasetTypeAnomaly.cable_swap_, 
        MVTecDatasetTypeAnomaly.combined_, 
        MVTecDatasetTypeAnomaly.cut_inner_insulation_, 
        MVTecDatasetTypeAnomaly.cut_outer_insulation_, 
        MVTecDatasetTypeAnomaly.missing_cable_, 
        MVTecDatasetTypeAnomaly.missing_wire_, 
        MVTecDatasetTypeAnomaly.poke_insulation_
        ],

    MVTecDatasetType.capsule_ : [
        MVTecDatasetTypeAnomaly.crack_, 
        MVTecDatasetTypeAnomaly.faulty_imprint_, 
        MVTecDatasetTypeAnomaly.poke_, 
        MVTecDatasetTypeAnomaly.scratch_, 
        MVTecDatasetTypeAnomaly.squeeze_
        ],

    MVTecDatasetType.carpet_ : [
        MVTecDatasetTypeAnomaly.color_, 
        MVTecDatasetTypeAnomaly.cut_, 
        MVTecDatasetTypeAnomaly.hole_, 
        MVTecDatasetTypeAnomaly.metal_contamination_, 
        MVTecDatasetTypeAnomaly.thread_
        ],

    MVTecDatasetType.grid_ : [
        MVTecDatasetTypeAnomaly.bent_, 
        MVTecDatasetTypeAnomaly.broken_, 
        MVTecDatasetTypeAnomaly.glue_, 
        MVTecDatasetTypeAnomaly.metal_contamination_, 
        MVTecDatasetTypeAnomaly.thread_
        ],

    MVTecDatasetType.hazelnut_ : [
        MVTecDatasetTypeAnomaly.crack_, 
        MVTecDatasetTypeAnomaly.cut_, 
        MVTecDatasetTypeAnomaly.hole_, 
        MVTecDatasetTypeAnomaly.print_
        ],

    MVTecDatasetType.leather_ : [
        MVTecDatasetTypeAnomaly.color_,
        MVTecDatasetTypeAnomaly.cut_, 
        MVTecDatasetTypeAnomaly.fold_, 
        MVTecDatasetTypeAnomaly.glue_,
        MVTecDatasetTypeAnomaly.poke_,
        ],

    MVTecDatasetType.metal_nut_ : [
        MVTecDatasetTypeAnomaly.bent_, 
        MVTecDatasetTypeAnomaly.color_, 
        MVTecDatasetTypeAnomaly.flip_,
        MVTecDatasetTypeAnomaly.scratch_,
        ],

    MVTecDatasetType.pill_ : [
        MVTecDatasetTypeAnomaly.color_,
        MVTecDatasetTypeAnomaly.combined_,
        MVTecDatasetTypeAnomaly.contamination_,
        MVTecDatasetTypeAnomaly.crack_,
        MVTecDatasetTypeAnomaly.faulty_imprint_,
        MVTecDatasetTypeAnomaly.pill_type_,
        MVTecDatasetTypeAnomaly.scratch_,
        ],

    MVTecDatasetType.screw_ : [
        MVTecDatasetTypeAnomaly.manipulated_front_,
        MVTecDatasetTypeAnomaly.scratch_head_,
        MVTecDatasetTypeAnomaly.scratch_neck_,
        MVTecDatasetTypeAnomaly.thread_side_,
        MVTecDatasetTypeAnomaly.thread_top_,
        ],

    MVTecDatasetType.tile_ : [
        MVTecDatasetTypeAnomaly.crack_,
        MVTecDatasetTypeAnomaly.glue_strip_,
        MVTecDatasetTypeAnomaly.gray_stroke_,
        MVTecDatasetTypeAnomaly.oil_,
        MVTecDatasetTypeAnomaly.rough_,
        ],

    MVTecDatasetType.toothbrush_ : [ 
        MVTecDatasetTypeAnomaly.defective_,
        ],

    MVTecDatasetType.transistor_ : [
        MVTecDatasetTypeAnomaly.bent_lead_,
        MVTecDatasetTypeAnomaly.cut_lead_,
        MVTecDatasetTypeAnomaly.damaged_case_,
        MVTecDatasetTypeAnomaly.misplaced_,
        ],

    MVTecDatasetType.wood_ : [
        MVTecDatasetTypeAnomaly.color_,
        MVTecDatasetTypeAnomaly.combined_,
        MVTecDatasetTypeAnomaly.hole_,
        MVTecDatasetTypeAnomaly.liquid_,
        MVTecDatasetTypeAnomaly.scratch_,
        ],

    MVTecDatasetType.zipper_ : [
        MVTecDatasetTypeAnomaly.broken_teeth_,
        MVTecDatasetTypeAnomaly.combined_,
        MVTecDatasetTypeAnomaly.fabric_border_,
        MVTecDatasetTypeAnomaly.fabric_interior_,
        MVTecDatasetTypeAnomaly.rough_,
        MVTecDatasetTypeAnomaly.split_teeth_,
        MVTecDatasetTypeAnomaly.squeezed_teeth_,
        ]
}

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
            # self.images_ = self.images_ + [self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]
            # self.images_name_ = self.images_name_ + dir_images
            self.images_.extend([self.image_unit_.LoadImage(path, color_mode).flatten() for path in dir_images]) # type: ignore
            self.images_name_.extend(dir_images) # type: ignore
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
            # self.images = self.images_ + [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]
            # self.images_name_ = self.images_name_ + dir_images
            self.images_.extend([self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]) # type: ignore
            self.images_name_.extend(dir_images) # type: ignore
        else:
            self.images_ = [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size).flatten() for path in dir_images]
            self.images_name_ = dir_images

        print(f"Loaded {len(dir_images)} images from {paths}")