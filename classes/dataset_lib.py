from typing import Final, Optional
from enum import Enum, unique
from os import listdir, makedirs
from os.path import isfile, join, exists, dirname
from cv2 import imread, imshow, waitKey, destroyAllWindows, imwrite, cvtColor, resize, IMREAD_COLOR, IMREAD_GRAYSCALE, INTER_NEAREST, INTER_LINEAR, INTER_CUBIC, INTER_LANCZOS4, COLOR_RGB2GRAY, COLOR_GRAY2RGB
from numpy import ndarray
from anomalib.data.image.folder import Folder, TestSplitMode
from anomalib import TaskType

from classes.util_lib import Size, Rect 

# Create a image processing class
class ImageUnit:
    """
    Agent for image operations.
    Used for loading, saving, resizing, converting color, and cropping images.

    Enum:
        ColorModeEnum : Enum for different color modes.
        ColorConversionEnum : Enum for different color conversions.
        ImageInterpolationEnum : Enum for different interpolation methods for image resizing.


    Methods:
        LoadImage : Load image from file.
        SaveImage : Save image to file.
        ResizeImage : Resize image.
        ConvertColor : Convert color of image.
        CropImage : Crop image.
        LoadVideo : Load video from file.
        FindPlantMask : Find plant mask in the image using color range.
        FindPlantContour : Find plant contour in the mask.

    :example:
    >>> image_unit : ImageUnit = ImageUnit()  
    >>> image : ndarray = image_unit.LoadImage("path/to/image.jpg", ColorMode.rgb)
    """
    @unique
    class ColorModeEnum(Enum):
        """
        Enum for different color modes for image processing.

        rgb_ : RGB color mode
        grayscale_ : Grayscale color mode
        """
        rgb_ = IMREAD_COLOR
        grayscale_ = IMREAD_GRAYSCALE

    # Enum for color conversion
    @unique
    class ColorConversionEnum(Enum):
        """
        Enum for different color conversion methods for image processing.

        rgb2gray_ : RGB to Grayscale conversion
        gray2rgb_ : Grayscale to RGB
        """
        rgb2gray_ = COLOR_RGB2GRAY
        gray2rgb_ = COLOR_GRAY2RGB

    @unique
    class ImageInterpolationEnum(Enum):
        """
        Enum for different interpolation methods for image resizing.

        nearest_ : Nearest neighbor interpolation
        linear_ : Linear interpolation
        cubic_ : Cubic interpolation
        lanczos4_ : Lanczos4 interpolation
        """
        nearest_ = INTER_NEAREST
        linear_ = INTER_LINEAR
        cubic_ = INTER_CUBIC
        lanczos4_ = INTER_LANCZOS4

    def __init__(self):
        ...
    
    def LoadImage(self, path: str, color_mode: ColorModeEnum) -> ndarray:
        """
        Load image from file.

        Args:
            path : (str) Path to the image file.
            color_mode : (ColorMode) Color mode of the image.

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
            path : (str) Path to save the image.
            image : (ndarray) Image data.

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

    def ResizeImage(self, image: ndarray, size: Size[int], interpolation: ImageInterpolationEnum = ImageInterpolationEnum.linear_) -> ndarray:
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

    def ConvertColor(self, image: ndarray, conversion: ColorConversionEnum) -> ndarray:
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

    Enum:
        MVTecDatasetTypeEnum : Enum for different MVTec dataset types.
        MVTecDatasetTypeAnomalyEnum : Enum for different MVTec dataset anomaly types.
    
    Dictionary:
        MVTecDataset : Dictionary for different MVTec dataset types and anomaly types.

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
    @unique
    class MVTecDatasetTypeEnum(Enum):
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
    class MVTecDatasetTypeAnomalyEnum(Enum):
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
    MVTecDataset : Final[dict[MVTecDatasetTypeEnum, list[MVTecDatasetTypeAnomalyEnum]]] = {
        MVTecDatasetTypeEnum.bottle_ : [
            MVTecDatasetTypeAnomalyEnum.broken_large_, 
            MVTecDatasetTypeAnomalyEnum.broken_small_, 
            MVTecDatasetTypeAnomalyEnum.contamination_
            ],

        MVTecDatasetTypeEnum.cable_ : [ 
            MVTecDatasetTypeAnomalyEnum.bent_wire_,
            MVTecDatasetTypeAnomalyEnum.cable_swap_, 
            MVTecDatasetTypeAnomalyEnum.combined_, 
            MVTecDatasetTypeAnomalyEnum.cut_inner_insulation_, 
            MVTecDatasetTypeAnomalyEnum.cut_outer_insulation_, 
            MVTecDatasetTypeAnomalyEnum.missing_cable_, 
            MVTecDatasetTypeAnomalyEnum.missing_wire_, 
            MVTecDatasetTypeAnomalyEnum.poke_insulation_
            ],

        MVTecDatasetTypeEnum.capsule_ : [
            MVTecDatasetTypeAnomalyEnum.crack_, 
            MVTecDatasetTypeAnomalyEnum.faulty_imprint_, 
            MVTecDatasetTypeAnomalyEnum.poke_, 
            MVTecDatasetTypeAnomalyEnum.scratch_, 
            MVTecDatasetTypeAnomalyEnum.squeeze_
            ],

        MVTecDatasetTypeEnum.carpet_ : [
            MVTecDatasetTypeAnomalyEnum.color_, 
            MVTecDatasetTypeAnomalyEnum.cut_, 
            MVTecDatasetTypeAnomalyEnum.hole_, 
            MVTecDatasetTypeAnomalyEnum.metal_contamination_, 
            MVTecDatasetTypeAnomalyEnum.thread_
            ],

        MVTecDatasetTypeEnum.grid_ : [
            MVTecDatasetTypeAnomalyEnum.bent_, 
            MVTecDatasetTypeAnomalyEnum.broken_, 
            MVTecDatasetTypeAnomalyEnum.glue_, 
            MVTecDatasetTypeAnomalyEnum.metal_contamination_, 
            MVTecDatasetTypeAnomalyEnum.thread_
            ],

        MVTecDatasetTypeEnum.hazelnut_ : [
            MVTecDatasetTypeAnomalyEnum.crack_, 
            MVTecDatasetTypeAnomalyEnum.cut_, 
            MVTecDatasetTypeAnomalyEnum.hole_, 
            MVTecDatasetTypeAnomalyEnum.print_
            ],

        MVTecDatasetTypeEnum.leather_ : [
            MVTecDatasetTypeAnomalyEnum.color_,
            MVTecDatasetTypeAnomalyEnum.cut_, 
            MVTecDatasetTypeAnomalyEnum.fold_, 
            MVTecDatasetTypeAnomalyEnum.glue_,
            MVTecDatasetTypeAnomalyEnum.poke_,
            ],

        MVTecDatasetTypeEnum.metal_nut_ : [
            MVTecDatasetTypeAnomalyEnum.bent_, 
            MVTecDatasetTypeAnomalyEnum.color_, 
            MVTecDatasetTypeAnomalyEnum.flip_,
            MVTecDatasetTypeAnomalyEnum.scratch_,
            ],

        MVTecDatasetTypeEnum.pill_ : [
            MVTecDatasetTypeAnomalyEnum.color_,
            MVTecDatasetTypeAnomalyEnum.combined_,
            MVTecDatasetTypeAnomalyEnum.contamination_,
            MVTecDatasetTypeAnomalyEnum.crack_,
            MVTecDatasetTypeAnomalyEnum.faulty_imprint_,
            MVTecDatasetTypeAnomalyEnum.pill_type_,
            MVTecDatasetTypeAnomalyEnum.scratch_,
            ],

        MVTecDatasetTypeEnum.screw_ : [
            MVTecDatasetTypeAnomalyEnum.manipulated_front_,
            MVTecDatasetTypeAnomalyEnum.scratch_head_,
            MVTecDatasetTypeAnomalyEnum.scratch_neck_,
            MVTecDatasetTypeAnomalyEnum.thread_side_,
            MVTecDatasetTypeAnomalyEnum.thread_top_,
            ],

        MVTecDatasetTypeEnum.tile_ : [
            MVTecDatasetTypeAnomalyEnum.crack_,
            MVTecDatasetTypeAnomalyEnum.glue_strip_,
            MVTecDatasetTypeAnomalyEnum.gray_stroke_,
            MVTecDatasetTypeAnomalyEnum.oil_,
            MVTecDatasetTypeAnomalyEnum.rough_,
            ],

        MVTecDatasetTypeEnum.toothbrush_ : [ 
            MVTecDatasetTypeAnomalyEnum.defective_,
            ],

        MVTecDatasetTypeEnum.transistor_ : [
            MVTecDatasetTypeAnomalyEnum.bent_lead_,
            MVTecDatasetTypeAnomalyEnum.cut_lead_,
            MVTecDatasetTypeAnomalyEnum.damaged_case_,
            MVTecDatasetTypeAnomalyEnum.misplaced_,
            ],

        MVTecDatasetTypeEnum.wood_ : [
            MVTecDatasetTypeAnomalyEnum.color_,
            MVTecDatasetTypeAnomalyEnum.combined_,
            MVTecDatasetTypeAnomalyEnum.hole_,
            MVTecDatasetTypeAnomalyEnum.liquid_,
            MVTecDatasetTypeAnomalyEnum.scratch_,
            ],

        MVTecDatasetTypeEnum.zipper_ : [
            MVTecDatasetTypeAnomalyEnum.broken_teeth_,
            MVTecDatasetTypeAnomalyEnum.combined_,
            MVTecDatasetTypeAnomalyEnum.fabric_border_,
            MVTecDatasetTypeAnomalyEnum.fabric_interior_,
            MVTecDatasetTypeAnomalyEnum.rough_,
            MVTecDatasetTypeAnomalyEnum.split_teeth_,
            MVTecDatasetTypeAnomalyEnum.squeezed_teeth_,
            ]
    }

    def __init__(self) -> None:
        """
        Initialize the dataset unit.
        """
        self.image_unit_ : ImageUnit = ImageUnit()
        self.images_ : list[ndarray] = []
        self.images_name_ : list[str] = []
        self.folder_ : Optional[Folder] = None

    def ClearDataset(self) -> None:
        """
        Clear the dataset.

        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.ClearDataset()
        """
        self.images_ = []
        self.images_name_ = []
        self.folder_ = None

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

    def LoadImages(self, paths: str, color_mode: ImageUnit.ColorModeEnum) -> None:
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

    def LoadImagesResize(self, paths: str, color_mode: ImageUnit.ColorModeEnum, size: Size) -> None:
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

    def LoadImagesResize2D(self, paths: str, color_mode: ImageUnit.ColorModeEnum, size: Size) -> None:
        """
        Load images from a specified directory, resize them to a specified size, and store them in the dataset.
        Images are stored as 2D arrays for further processing.
        Image names are stored for reference.

        Args:
            paths (str): Path to the directory.
            color_mode (ColorMode): Color mode of the images.
            size (Size): Size to resize the images.
        
        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.LoadImagesResize2D("path/to/images", ColorMode.rgb, Size(100, 100))
        """
        dir_images : list[str] = self.DirImages(paths)
        if len(dir_images) == 0:
            print("No images found in the directory")
            return
        if len(self.images_) > 0:
            self.images_.extend([self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size) for path in dir_images])
            self.images_name_.extend(dir_images)
        else:
            self.images_ = [self.image_unit_.ResizeImage(self.image_unit_.LoadImage(path, color_mode), size) for path in dir_images]
            self.images_name_ = dir_images

        print(f"Loaded {len(dir_images)} images from {paths}")

    
    def AnomalibLoadFolder(self, *,root_path : str, normal_path : list[str], normal_test_path : Optional[list[str]], abnormal_path : Optional[list[str]], normal_split_ratio : float,test_split_ratio : float, datalib_name : str, size : Size, task : TaskType) -> None:
        """
        Load images from a specified directory, resize them to a specified size, and store them in the dataset.
        
        Args:
            root_path (str): Path to the root directory.
            normal_path (list[str]): List of paths to the normal images.
            abnormal_path (list[str]): List of paths to the abnormal images.
            normal_test_split_ratio (float): Ratio of normal images to be used for testing.
            datalib_name (str): Name of the dataset.
            size (Size): Size to resize the images.
            task (TaskType): Task type of the dataset.
        
        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.AnomalibLoadFolder(
        >>>     root_path="datasets/bottle",
        >>>     normal_path=["train/good"],
        >>>     abnormal_path=["test/broken_large", "test/broken_small", "test/contamination"],
        >>>     normal_test_split_ratio=0.2,
        >>>     datalib_name="bottle",
        >>>     size=Size(64, 64),
        >>>     task=TaskType.CLASSIFICATION
        >>> )
        """
        self.folder_ = Folder(
            name=datalib_name,
            root=root_path,
            normal_dir=normal_path,
            abnormal_dir=abnormal_path,
            normal_test_dir=normal_test_path,
            normal_split_ratio=normal_split_ratio,
            test_split_ratio=test_split_ratio,
            image_size=(size.width_, size.height_),
            train_batch_size=32,
            eval_batch_size=32,
            num_workers=2,
            task=task.value,
        )
        self.folder_.setup()

    def AnomalibDatasetValidation(self) -> None:
        """
        Validate the dataset.

        :example:
        >>> dataset_unit : DatasetUnit = DatasetUnit()
        >>> dataset_unit.AnomalibDatasetValidation() # Output: Folder not initialized
        """
        assert isinstance(self.folder_, Folder), "Folder not initialized"
