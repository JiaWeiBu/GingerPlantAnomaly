from typing import Optional
from enum import Enum, unique, auto
from classes.dataset_lib import DatasetUnit
from anomalib.deploy.inferencers import TorchInferencer
from anomalib.utils.visualization.image import ImageResult
from matplotlib import pyplot as plt
import numpy as np
from math import ceil
from matplotlib import gridspec
from io import BytesIO
from PIL import Image

class ModelPathUnit:
    """
    The ModelPathUnit class is used to manage model paths and types.
    It provides methods to validate model types and weeks, and to generate model paths.

    Enums:
    ModelTypeEnum : Enum - Enum for model paths.
    ModelWeekEnum : Enum - Enum for model weeks.

    Methods:
    ModelPath(type: ModelTypeEnum, week: ModelWeekEnum) -> str - Get the model path.
    IsValidWeek(week: int) -> Optional[ModelWeekEnum] - Check if the week is valid and return the corresponding enum.
    IsValidModel(name: str) -> Optional[ModelTypeEnum] - Check if the model name is valid and return the corresponding enum.
    IsValid(types: str, week: int) -> Optional[tuple[ModelTypeEnum, ModelWeekEnum]] - Check if the model type and week are valid and return the corresponding enums.
    """

    @unique
    class ModelTypeEnum(Enum):
        """
        Enum for model paths.

        Attributes:
        cflow_ : str - Path to the cflow model.
        fastflow_ : str - Path to the fastflow model.
        patchcore_ : str - Path to the patchcore model.
        reversedistillation_ : str - Path to the reversedistillation model.
        stpm_ : str - Path to the stpm model.
        """
        cflow_ = auto()
        fastflow_ = auto()
        patchcore_ = auto()
        reverse_distillation_ = auto()
        stfpm_ = auto()



    @unique
    class ModelWeekEnum(Enum):
        """
        Enum for model weeks.

        Attributes:
        week3_ : str - Path to the week 3 model.
        week8_ : str - Path to the week 8 model.
        week12_ : str - Path to the week 12 model.
        week18_ : str - Path to the week 18 model.
        """
        week3_ = 3
        week8_ = 8
        week12_ = 12
        week18_ = 18
    
    def ModelPath(self, types: ModelTypeEnum, week: ModelWeekEnum) -> str:
        """
        Get the model path.

        Args:
        type : ModelTypeEnum - The type of the model.
        week : ModelWeekEnum - The week of the model.

        Returns:
        str - The model path.
        """
        return f"models/T5_Full_Individual_Filtered_Week_Unseen_Week{week.value}_Save_SimMutiAnomaly/{types.name}/weights/torch/model.pt"
    
    def IsValidWeek(self, week: int) -> Optional[ModelWeekEnum]:
        """
        Check if the week is valid and return the corresponding enum.

        Args:
        week : int - The week to check.

        Returns:
        Optional[ModelWeekEnum] - The corresponding enum if valid, None otherwise.
        """
        for week_enum in self.ModelWeekEnum:
            if week_enum.value == week:
                return week_enum
        return None
    
    def IsValidModel(self, name: str) -> Optional[ModelTypeEnum]:
        """
        Check if the model name is valid and return the corresponding enum.

        Args:
        name : str - The model name to check (underscores and spaces removed, case-insensitive).

        Returns:
        Optional[ModelTypeEnum] - The corresponding enum if valid, None otherwise.
        """
        normalized_name = name.replace("_", "").replace(" ", "").lower()
        for model_enum in self.ModelTypeEnum:
            #print(f"Checking {model_enum.name.replace('_', '').lower()} against {normalized_name}")
            if model_enum.name.replace("_", "").lower() == normalized_name:
                return model_enum
        return None
    
    def IsValid(self, *, types: str, week: int) -> Optional[tuple[ModelTypeEnum, ModelWeekEnum]]:
        """
        Check if the model type and week are valid and return the corresponding enums.

        Args:
        type : str - The model type to check.
        week : int - The week to check.

        Returns:
        Optional[tuple[ModelTypeEnum, ModelWeekEnum]] - A tuple of the corresponding enums if valid, None otherwise.
        """
        model_enum = self.IsValidModel(types)
        week_enum = self.IsValidWeek(week)
        if model_enum and week_enum:
            return model_enum, week_enum
        return None
    

class AnomalibTest:
    """
    The AnomalibTest class is used to test the model for the Anomalib library.

    Attributes:
    param_ : DatasetUnit - The dataset unit to be used for testing.
    """

    def __init__(self) -> None:
        """
        Initialize the AnomalibTest class.

        Attributes:
        inferencer_ : Optional[TorchInferencer] - The inferencer to be used for testing.

        Example:
        >>> model_path_unit = ModelPathUnit()
        >>> anomalib_test = AnomalibTest()
        >>> anomalib_test.Setup(model_path=model_path_unit.ModelPath(type=ModelPathUnit.ModelTypeEnum.cflow_, week=ModelPathUnit.ModelWeekEnum.week3_))
        >>> anomalib_test.Evaluate(image_path="path/to/image.jpg")
        >>> anomalib_test.Evaluate(image_path="path/to/directory")
        """
        self.inferencer_: Optional[TorchInferencer] = None

    def Setup(self, *, model_path: str) -> None:
        """
        Setup the model path.

        Args:
        model_path : str - Path to the trained model.

        Example:
        >>> model_path_unit = ModelPathUnit()
        >>> anomalib_test = AnomalibTest()
        >>> anomalib_test.Setup(model_path=model_path_unit.ModelPath(type=ModelPathUnit.ModelTypeEnum.cflow_, week=ModelPathUnit.ModelWeekEnum.week3_))
        """
        self.inferencer_ = TorchInferencer(path=model_path)
    
    def Evaluate(self, *, image_path: str) -> list[tuple[Image.Image, str]]:
        """
        Evaluate the model on the test data.

        Args:
        image_path : str - Path to the image to be evaluated, can be a directory or a single image.

        Returns:
        list[tuple[Image.Image, str]] - A list of tuples containing the PIL image and the attributes as a string.
        """
        assert self.inferencer_ is not None, "Inferencer is not set"

        dataset_unit = DatasetUnit()
        dataset_unit.LoadImagesName(paths=image_path)
        
        results: list[tuple[Image.Image, str]] = []

        for image in dataset_unit.images_name_:
            result: ImageResult = self.inferencer_.predict(image)

            # Collect np.ndarray attributes for combined display
            images_to_display = []
            titles = []
            attributes_output = []

            for attr_name, attr_value in vars(result).items():
                if isinstance(attr_value, np.ndarray):
                    images_to_display.append(attr_value)
                    titles.append(attr_name)
                elif isinstance(attr_value, (float, str)):
                    attributes_output.append(f"{attr_name}: {attr_value}")

            # Combine all attributes into a single string
            attributes_string = "\n".join(attributes_output) + "\n"

            # Combine and display images
            if images_to_display:
                num_images = len(images_to_display)
                rows = ceil(num_images / 3)
                cols = min(num_images, 3)

                fig = plt.figure(figsize=(cols * 5, rows * 5))
                spec = gridspec.GridSpec(rows, cols, figure=fig, wspace=0.3, hspace=0.3)

                for idx, (img, title) in enumerate(zip(images_to_display, titles)):
                    ax = fig.add_subplot(spec[idx])
                    ax.imshow(img)
                    ax.set_title(f"Variable: {title}", fontsize=10)  # Add variable name at the top
                    ax.axis("off")

                # Add a white border around the entire figure
                fig.patch.set_facecolor('white')
                fig.tight_layout(pad=0)

                # Convert the matplotlib figure to a PIL image
                buf = BytesIO()
                fig.savefig(buf, format="png", bbox_inches='tight')
                buf.seek(0)
                pil_image = Image.open(buf).copy()  # Copy the image into memory
                buf.close()

                # Append the PIL image and attributes string to the results list
                results.append((pil_image, attributes_string))

        return results
            
def main():
    """
    Run the testing sequence directly from this file.
    """
    print("Starting the testing sequence...")
    model_path_unit = ModelPathUnit()
    anomalib_test = AnomalibTest()
    anomalib_test.Setup(model_path=model_path_unit.ModelPath(types=ModelPathUnit.ModelTypeEnum.cflow_, week=ModelPathUnit.ModelWeekEnum.week3_))
    result: list[tuple[Image.Image, str]] = anomalib_test.Evaluate(image_path="testtest/test")

    # show the image with the title be the string
    for img, title in result:
        img.show(title=title)
        print(title)

if __name__ == "__main__":
    main()