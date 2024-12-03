from classes.anomalib_lib import AnomalyModelUnit
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size, TimeIt
from classes.progress_lib import ProgressUnit
from time import time
from os.path import exists
from os import makedirs

DATASET_PATH = "./datasets"
GOOD_PATH = ["train/good", "test/good"]
Previous : bool = True

def AbnormalPathGen(DatasetType : DatasetUnit.MVTecDatasetTypeEnum) -> list[str]:
    return [f"test/{anomaly.value}" for anomaly in DatasetUnit.MVTecDataset[DatasetType]]

#@TimeIt
def main():
    # progress_unit : ProgressUnit = ProgressUnit()
    # if Previous:
    #     progress_unit.read_progress()
    # else:
    #     progress_unit.new_progress()
    #     with open("anomalib_results.txt", "w", encoding="utf-8") as f:
    #         f.write("dataset_type, model_type, AUROC, AUPR, Time\n")
    #     with open("anomalib_log.log", "w", encoding="utf-8") as f:
    #         f.write("Log File\n")

    
    # # # Load the data from each dataset type
    # for dataset_type in DatasetUnit.MVTecDatasetTypeEnum:
    # #for dataset_type in [DatasetUnit.MVTecDatasetTypeEnum.bottle_]:
    #     # Load the data from the dataset
    #     print(f"Loading {dataset_type.value}")
    #     dataset_unit : DatasetUnit = DatasetUnit()
    #     dataset_unit.AnomalibLoadFolder(root_path = f"{DATASET_PATH}/{dataset_type.value}", normal_path=GOOD_PATH, abnormal_path=AbnormalPathGen(dataset_type), normal_test_split_ratio=0.2, datalib_name=dataset_type.value, size=Size(64, 64), task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_)
    #     dataset_unit.AnomalibDatasetValidation()
    #     print(f"Loaded {dataset_type.value}")

    #     # Load model for each model type
    #     for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
    #         if progress_unit.progression_matrix_[dataset_type][model_type]:
    #             print(f"{dataset_type.value}_{model_type.name}_passed")
    #             continue
    #         # Create the model
    #         try:
    #             start : float = time()
    #             print(f"Training {dataset_type.value} with {model_type.name}")
    #             anomaly_model : AnomalyModelUnit = AnomalyModelUnit(model_type=model_type, image_metrics=["AUROC", "AUPR"])
    #             anomaly_model.Train(datamodule=dataset_unit.folder_)
    #             result = anomaly_model.Evaluate(datamodule=dataset_unit.folder_)

    #             with open("anomalib_results.txt", "a", encoding="utf-8") as f:
    #                 f.write(f"{dataset_type.value},{model_type.value},{result[0]['image_AUROC']},{result[0]['image_AUPR']},{time() - start}\n")
    #                 print("result added")
                
    #             progress_unit.update_progress(dataset_type, model_type)

    #             # save model in models/data_type/model_type
    #             # check if the directory exists
    #             # if not create it
    #             if not exists(f"models/{dataset_type.value}"):
    #                 makedirs(f"models/{dataset_type.value}")
    #             if not exists(f"models/{dataset_type.value}/{model_type.name}"):
    #                 makedirs(f"models/{dataset_type.value}/{model_type.name}")
    #             anomaly_model.Save(f"models/{dataset_type.value}/{model_type.name}")

    #         except Exception as e:
    #             with open("anomalib_log.log", "a", encoding="utf-8") as f:
    #                 f.write(f"Dataset Type: {dataset_type.value}\nModel Type: {model_type.value}\nError: {e}\n\n")
    #             continue


    with open("plant_anomalib_results5.txt", "w", encoding="utf-8") as f:
        f.write("dataset_type, model_type, AUROC, AUPR, Time\n")
    with open("plant_anomalib_log.log", "w", encoding="utf-8") as f:
        f.write("Log File\n")

    # load plant data from the dataset
    train_unit : DatasetUnit = DatasetUnit()
    train_unit.AnomalibLoadFolder(root_path=f"{DATASET_PATH}/re_plant", normal_path=["train/top","train/60",], normal_test_path=["good/top","good/60"], abnormal_path=["bad/60", "bad/top"], normal_split_ratio=0.0, test_split_ratio=0.0, datalib_name="plant",size=Size[int](64, 64), task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_)
    train_unit.AnomalibDatasetValidation()
    print(f"Loaded plant train")

    # test_unit : DatasetUnit = DatasetUnit()
    # test_unit.AnomalibLoadFolder(root_path=f"{DATASET_PATH}", normal_path=["plant/week3/60","plant/week3/top","bg_rip/week3/60","bg_rip/week3/top"], abnormal_path=["zombie/week3/60", "zombie/week3/top"], normal_test_split_ratio=100, datalib_name="plant",size=Size[int](64, 64), task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_)
    # test_unit.AnomalibDatasetValidation()
    # print(f"Loaded plant test")

    for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
        # Create the model
        try:
            start : float = time()
            print(f"Training plant with {model_type.name}")
            anomaly_model : AnomalyModelUnit = AnomalyModelUnit(model_type=model_type, image_metrics=["AUROC", "AUPR"])
            anomaly_model.Train(datamodule=train_unit.folder_)
            result = anomaly_model.Evaluate(datamodule=train_unit.folder_)

            with open("plant_anomalib_results5.txt", "a", encoding="utf-8") as f:
                f.write(f"plant,{model_type.value},{result[0]['image_AUROC']},{result[0]['image_AUPR']},{time() - start}\n")
                print("result added")
            
            # save model in models/data_type/model_type
            # check if the directory exists
            # if not create it
            if not exists(f"models/plant"):
                makedirs(f"models/plant")
            if not exists(f"models/plant/{model_type.name}"):
                makedirs(f"models/plant/{model_type.name}")
            anomaly_model.Save(f"models/plant/{model_type.name}")
        
        except Exception as e:
            with open("plant_anomalib_log.log", "a", encoding="utf-8") as f:
                f.write(f"Dataset Type: plant\nModel Type: {model_type.value}\nError: {e}\n\n")
            continue

if __name__ == '__main__':
    main()