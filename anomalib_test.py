# run testing on all model
# model location in models/data_type/model_type/weights/torch/model.pt

from pandas import DataFrame
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size
from classes.anomalib_lib import AnomalyModelUnit
import torch

DATASET_PATH = "./datasets"

def LoadMVTecData(*, dataset_type: DataFrame.MVTecDatasetTypeEnum, size: Size[int], config : bool = False, colour_mode : ImageUnit.ColorModeEnum = ImageUnit.ColorModeEnum.grayscale_) -> tuple[DataFrame, DataFrame]:
    if config:
        print("Loading Data")

    test_good_module = DatasetUnit()
    test_good_module.LoadImagesResize2D(f"{DATASET_PATH}/{dataset_type.value}/test/good", colour_mode, size)

    test_defective_module = DatasetUnit()
    for anomaly in DatasetUnit.MVTecDataset[dataset_type]:
        test_defective_module.LoadImagesResize2D(f"{DATASET_PATH}/{dataset_type.value}/test/{anomaly.value}", colour_mode, size)

    test_good = DataFrame(test_good_module.images_)
    test_defective = DataFrame(test_defective_module.images_)

    print("Test Good Shape: ", test_good.shape)
    print("Test Defective Shape: ", test_defective.shape)

    if config:
        print("Data Loaded")

    return test_good, test_defective


def main():
    anomaly_model_unit = AnomalyModelUnit()
    for dataset_type in DatasetUnit.MVTecDatasetTypeEnum:
        print(f"Loading {dataset_type.value}")
        test_good, test_defective = LoadMVTecData(dataset_type=dataset_type, size=Size(64, 64), config=True)
        print(f"Loaded {dataset_type.value}")

        for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
            model = AnomalyModelUnit.PyTorchModelDict[model_type]()
            model.load_state_dict(torch.load(f"models/{dataset_type.value}/{model_type.name}/weights/torch/model.pt"))
            model.eval()
            print(f"Testing {dataset_type.value} with {model_type.name}")

            # Test the model
            if anomaly_model_unit.ModelValid(model_type=model_type):
                output_good = model(test_good)
                output_defective = model(test_defective)
                print(f"Output Good Shape: {output_good.shape}")
                print(f"Output Defective Shape: {output_defective.shape}")
                print (f"Output Good: {output_good}")
                print (f"Output Defective: {output_defective}")

    

if __name__ == '__main__':
    main()