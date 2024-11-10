
from pandas import DataFrame
from classes.pycaret_lib import PyCaretModelUnit # type: ignore
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size, Unused

DATASET_PATH = "./datasets"

def LoadData(*, train_path: str, test_good_path: str, test_defective_path: str, size: Size[int], config : bool = False, colour_mode : ImageUnit.ColorModeEnum = ImageUnit.ColorModeEnum.grayscale_) -> tuple[DataFrame, DataFrame, DataFrame]:
    if config:
        print("Loading Data")

    train_module = DatasetUnit()
    train_module.LoadImagesResize(train_path, colour_mode, size)

    test_good_module = DatasetUnit()
    test_good_module.LoadImagesResize(test_good_path, colour_mode, size)
    
    test_defective_module = DatasetUnit()
    test_defective_module.LoadImagesResize(test_defective_path, colour_mode, size)

    if config:
        print("Converting to DataFrame")
        
    train = DataFrame(train_module.images_)
    test_good = DataFrame(test_good_module.images_)
    test_defective = DataFrame(test_defective_module.images_)

    print("Train Shape: ", train.shape)
    print("Test Good Shape: ", test_good.shape)
    print("Test Defective Shape: ", test_defective.shape)

    if config:
        print("Data Loaded")

    return train, test_good, test_defective

def LoadMVTecData(*, dataset_type: DataFrame.MVTecDatasetTypeEnum, size: Size[int], config : bool = False, colour_mode : ImageUnit.ColorModeEnum = ImageUnit.ColorModeEnum.grayscale_) -> tuple[DataFrame, DataFrame, DataFrame]:
    if config:
        print("Loading Data")

    train_module = DatasetUnit()
    train_module.LoadImagesResize(f"{DATASET_PATH}/{dataset_type.value}/train/good", colour_mode, size)

    test_good_module = DatasetUnit()
    test_good_module.LoadImagesResize(f"{DATASET_PATH}/{dataset_type.value}/test/good", colour_mode, size)

    test_defective_module = DatasetUnit()
    for anomaly in DatasetUnit.MVTecDataset[dataset_type]:
        test_defective_module.LoadImagesResize(f"{DATASET_PATH}/{dataset_type.value}/test/{anomaly.value}", colour_mode, size)

    train = DataFrame(train_module.images_)
    test_good = DataFrame(test_good_module.images_)
    test_defective = DataFrame(test_defective_module.images_)

    print("Train Shape: ", train.shape)
    print("Test Good Shape: ", test_good.shape)
    print("Test Defective Shape: ", test_defective.shape)

    if config:
        print("Data Loaded")

    return train, test_good, test_defective

def PycaretTrainTestSequence(*,model : PyCaretModelUnit, train : DataFrame, test_good : DataFrame, test_defective : DataFrame, dataset_type : DatasetUnit.MVTecDatasetTypeEnum, model_type : PyCaretModelUnit.PyCaretModelTypeEnum, size : str) -> None:
    model.Train(data=train, model_type=model_type)
    #model.Evaluate()
    #model.Plot(PlotType.tsne_)
    #model.Save(f"{model_type.value}_model_{size}")
    # model.Results(test_good, "knn_model_good_1")
    # model.Results(test_defective, "knn_model_defective_1")
    Unused(size)
    model.EvaluationMetrics(test_good, test_defective, f"{dataset_type.value}_{model_type.value}")

def main():
    # Train Model
    # For each ModelType in ModelType Enum, train the model and save it log error
    with open('./results/error.log', 'w', encoding='utf-8') as f:
        f.write("")

    with open('./results/result.csv', 'w', encoding='utf-8') as f:
        f.write("Model,Accuracy,Precision,Recall,F1-score\n")

    image_size : Size[int] = Size[int](64, 64)

    #Load Data from each MVTec Dataset Type
    for dataset_type in DatasetUnit.MVTecDatasetTypeEnum:
        with open('./results/result.csv', 'a', encoding='utf-8') as f:
            f.write(f"\nType: {dataset_type}\n")
        
        # Load Data
        train, test_good, test_defective = LoadMVTecData(dataset_type=dataset_type, size=image_size, config=True)

    
        print("Training Models")
        total_model = len(PyCaretModelUnit.PyCaretModelTypeEnum)
        count = 1
        for model_type in PyCaretModelUnit.PyCaretModelTypeEnum:
            try:
                print(f"Training {dataset_type.value} on {model_type.value} model {count}/{total_model}")
                model = PyCaretModelUnit()
                PycaretTrainTestSequence(model=model, train=train, test_good=test_good, test_defective=test_defective, dataset_type=dataset_type, model_type=model_type, size=image_size)

                count += 1
            except Exception as e:
                print(f"Error training for {dataset_type.value} on {model_type.value} model: {e}")
                with open('./results/error.log', 'a', encoding='utf-8') as f:
                    f.write(f"Error training for {dataset_type.value} on {model_type.value} model: {e}\n")
                continue


if __name__ == "__main__":
    main()