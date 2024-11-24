# run testing on all model
# model location in models/data_type/model_type/weights/torch/model.pt

from typing import Any
import torch
from numpy import asarray
import torchvision.transforms as transforms
from pandas import DataFrame
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size
from classes.anomalib_lib import AnomalyModelUnit

from anomalib.deploy.inferencers import TorchInferencer
from matplotlib import pyplot as plt
from anomalib.utils.visualization.image import ImageResult

DATASET_PATH = "./datasets"

def LoadMVTecData(*, dataset_type: DatasetUnit.MVTecDatasetTypeEnum, size: Size[int], config : bool = False, colour_mode : ImageUnit.ColorModeEnum = ImageUnit.ColorModeEnum.grayscale_) -> tuple[Any, Any]:
    if config:
        print("Loading Data")

    test_good_module = DatasetUnit()
    test_good_module.LoadImagesResize2D(f"{DATASET_PATH}/{dataset_type.value}/test/good", colour_mode, size)

    test_defective_module = DatasetUnit()
    for anomaly in DatasetUnit.MVTecDataset[dataset_type]:
        test_defective_module.LoadImagesResize2D(f"{DATASET_PATH}/{dataset_type.value}/test/{anomaly.value}", colour_mode, size)

    # test_good = DataFrame(test_good_module.images_)
    # test_defective = DataFrame(test_defective_module.images_)

    # print("Test Good Shape: ", test_good.shape)
    # print("Test Defective Shape: ", test_defective.shape)
    test_good = test_good_module.images_
    test_defective = test_defective_module.images_

    if config:
        print("Data Loaded")

    return test_good, test_defective


def main():
    transform_ = transforms.Compose([
        transforms.ToTensor()
    ])


    anomaly_model_unit = AnomalyModelUnit()
    for dataset_type in DatasetUnit.MVTecDatasetTypeEnum:
        print(f"Loading {dataset_type.value}")
        print(f"Loaded {dataset_type.value}")

        for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
            # Test the model
            if anomaly_model_unit.ModelValid(model_type=model_type):
                inferencers = TorchInferencer(path=f"models/{dataset_type.value}/{model_type.name}/weights/torch/model.pt")
                print(f"Testing {dataset_type.value} with {model_type.name}")

                result : ImageResult = inferencers.predict("./datasets/bottle/test/broken_large/000.png")
                print(result.pred_label)
              


                print("k")


if __name__ == '__main__':
    main()