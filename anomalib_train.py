from os.path import exists
from os import makedirs
from typing import Any
from classes.general_lib import TrainObject, TrainPathObject#, PredictPathObject
from classes.dataset_lib import ImageUnit
from classes.util_lib import Size
from classes.anomalib_lib import AnomalyModelUnit
from classes.dataset_lib import DatasetUnit


class AnomalibTrain:
    """
    The AnomalibTrain class is used to train the model for the Anomalib library.

    Attributes:
    param_ : TrainObject - The TrainObject containing the parameters for training the model.
    model_ : AnomalyModelUnit - The AnomalyModelUnit object.
    model_type_flag_ : AnomalyModelUnit.ModelTypeFlag - The model type flag for the AnomalyModelUnit.
    dataset_unit_ : DatasetUnit - The DatasetUnit object.

    Example:
    >>> param = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
    >>> model_type_flag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
    >>> anomalib_train = AnomalibTrain(param = param, model_type_flag = model_type_flag)
    """

    def __init__(self, *, param : TrainObject, model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_) -> None:
        """
        Initialize the AnomalibTrain class.

        TODO : Missing Config

        Args:
        param : TrainObject - The TrainObject containing the parameters for training the model.
        model_type_flag : AnomalyModelUnit.ModelTypeFlag - The model type flag for the AnomalyModelUnit.

        Attributes:
        param : TrainObject - The TrainObject containing the parameters for training the model.
        model_ : AnomalyModelUnit - The AnomalyModelUnit object.
        model_type_flag_ : AnomalyModelUnit.ModelTypeFlag - The model type flag for the AnomalyModelUnit.

        Example:
        >>> param = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train = AnomalibTrain(param = param, model_type_flag = model_type_flag)
        """
        self.param_ : TrainObject = param
        self.model_ : AnomalyModelUnit = AnomalyModelUnit()
        self.model_type_flag_ : AnomalyModelUnit.ModelTypeFlag = model_type_flag
        self.dataset_unit_ : DatasetUnit = DatasetUnit()

    def LoadData(self) -> None:
        """
        Load the data for training the model.

        Example:
        >>> param : TrainObject = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train : AnomalibTrain = AnomalibTrain(param=param, model_type_flag=model_type_flag)
        >>> anomalib_train.LoadData()
        """
        print("Loading Data")

        self.dataset_unit_.AnomalibLoadFolder(root_path=self.param_.path_.root_, normal_path=[self.param_.path_.train_], normal_test_path=[self.param_.path_.test_good_], abnormal_path=[self.param_.path_.test_defective_], normal_split_ratio=0.0, test_split_ratio=0.0, datalib_name=self.param_.name_, size=self.param_.size_, task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_.value)
        self.dataset_unit_.AnomalibDatasetValidation()

        print("Data Loaded")

    def TrainTestSequence(self, *, model_type : AnomalyModelUnit.ModelTypeFlag) -> Any:
        """
        Train the model and evaluate it.

        Args:
        model_type : AnomalyModelUnit.ModelTypeFlag - The model type flag for the AnomalyModelUnit.

        Returns:
        Any - The result of the evaluation.

        Example:
        >>> param : TrainObject = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train : AnomalibTrain = AnomalibTrain(param=param, model_type_flag=model_type_flag)
        >>> anomalib_train.LoadData()
        >>> result = anomalib_train.TrainTestSequence(model_type=AnomalyModelUnit.ModelTypeFlag.padim_)
        """
        anomaly_model : AnomalyModelUnit = AnomalyModelUnit(model_type=model_type, image_metrics=["AUROC", "AUPR"])
        assert self.dataset_unit_.folder_ is not None, "Dataset not loaded"
        anomaly_model.Train(datamodule=self.dataset_unit_.folder_)
        result = anomaly_model.Evaluate(datamodule=self.dataset_unit_.folder_)

        if not exists(self.param_.path_.model_save_):
            makedirs(self.param_.path_.model_save_)
        anomaly_model.Save(self.param_.path_.model_save_)

        return result

    def Run(self) -> None:
        """
        Run the training sequence.

        Example:
        >>> param : TrainObject = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train : AnomalibTrain = AnomalibTrain(param=param, model_type_flag=model_type_flag)
        >>> anomalib_train.Run()
        """
        self.LoadData()

        for model_type in self.model_type_flag_:
            try:
                print(f"Training {self.param_.name_} on {model_type.value} model")
                result = self.TrainTestSequence(model_type=model_type)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error training for {self.param_.name_} on {model_type.value} model: {e}")
            continue

class AnomalibTest:
    """
    The AnomalibTest class is used to test the model for the Anomalib library.

    Unimplemented as of now.
    """

    def __init__(self) -> None:
        ...

def main():
    train_object : TrainObject = TrainObject(path=TrainPathObject(root='datasets/re_plant', train=['train/60', 'train/top'], test_good=['good/60', 'good/top'], test_defective=['bad/60', "bad/top"], model_save='model_save_path'), name='dataset_name', size=Size(width=256, height=256), colour_mode=ImageUnit.ColorModeEnum.rgb_)
    model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_    
    anomalib_train : AnomalibTrain = AnomalibTrain(param=train_object, model_type_flag=model_type_flag)
    anomalib_train.Run()

if __name__ == "__main__":
    main()