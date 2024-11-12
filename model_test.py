

from classes.anomalib_lib import AnomalyModelUnit
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size
from classes.progress_lib import ProgressUnit

DATASET_PATH = "./datasets"
GOOD_PATH = ["train/good", "test/good"]
Previous : bool = False

def AbnormalPathGen(DatasetType : DatasetUnit.MVTecDatasetTypeEnum) -> list[str]:
    return [f"test/{anomaly.value}" for anomaly in DatasetUnit.MVTecDataset[DatasetType]]

def main():
    with open("anomalib_results.txt", "w") as f:
        f.write("dataset_type, model_type, AUROC, AUPRO, AUPR\n")
    with open("anomalib_log.log", "w") as f:
        f.write("Log File\n")

    progress_unit : ProgressUnit = ProgressUnit()
    if Previous:
        progress_unit.read_progress()
    else:
        progress_unit.new_progress()
    
    # # Load the data from each dataset type
    for dataset_type in [DatasetUnit.MVTecDatasetTypeEnum.bottle_]:
        # Load the data from the dataset
        dataset_unit : DatasetUnit = DatasetUnit()
        dataset_unit.AnomalibLoadFolder(root_path = f"{DATASET_PATH}/{dataset_type.value}", normal_path=GOOD_PATH, abnormal_path=AbnormalPathGen(dataset_type), normal_test_split_ratio=0.2, datalib_name=dataset_type.value, size=Size(64, 64), task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_)
        dataset_unit.AnomalibDatasetValidation()

        # Load model for each model type
        for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
            # Create the model
            try:
                anomaly_model : AnomalyModelUnit = AnomalyModelUnit(model_type=model_type, image_metrics=["AUROC","AUPRO", "AUPR"])
                anomaly_model.Train(datamodule=dataset_unit.folder_)
                result = anomaly_model.Evaluate(datamodule=dataset_unit.folder_)

                with open("anomalib_results.txt", "a") as f:
                    f.write(f"{dataset_type.value}, {model_type.value}, {result['image_AUROC']}, {result['image_AUPRO']}, {result['image_AUPR']}\n")
                    print(f"{dataset_type.value}, {model_type.value}, {result['image_AUROC']}, {result['image_AUPRO']}, {result['image_AUPR']}\n")
                    print("result added")
                
                progress_unit.update_progress(dataset_type, model_type)

            except Exception as e:
                with open("anomalib_log.log", "a") as f:
                    f.write(f"Dataset Type: {dataset_type.value}\nModel Type: {model_type.value}\nError: {e}\n\n")
                continue


    # # the above code is for all the datasets and all the models
    # # i want to run on bottle dataset and patchcore model
    # dataset_unit : DatasetUnit = DatasetUnit()
    # dataset_unit.AnomalibLoadFolder(root_path = f"{DATASET_PATH}/{DatasetUnit.MVTecDatasetTypeEnum.bottle_.value}", normal_path=GOOD_PATH, abnormal_path=AbnormalPathGen(DatasetUnit.MVTecDatasetTypeEnum.bottle_), normal_test_split_ratio=0, datalib_name="bottle", size=Size(64, 64), task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_)
    # dataset_unit.AnomalibDatasetValidation()

    # anomaly_model : AnomalyModelUnit = AnomalyModelUnit(model_type=AnomalyModelUnit.AnomalyModelTypeEnum.padim_, image_metrics=["AUROC","AUPR"])
    # anomaly_model.Train(datamodule=dataset_unit.folder_)
    # result = anomaly_model.Evaluate(datamodule=dataset_unit.folder_)
    # print(result)


if __name__ == '__main__':
    main()