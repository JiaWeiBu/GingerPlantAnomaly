from os.path import exists
from os import makedirs
from typing import Any, Optional
from asyncio import sleep
from classes.general_lib import TrainObject, TrainPathObject#, PredictPathObject
from classes.dataset_lib import ImageUnit
from classes.util_lib import Size
from classes.anomalib_lib import AnomalyModelUnit
from classes.dataset_lib import DatasetUnit
from classes.log_lib import LoggerTemplate, AsyncLoggerTemplate, LoggerDiscord

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

    def __init__(self, *, param : TrainObject, model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_, logger_async : bool, logger_instance : Optional[LoggerTemplate], logger_instance_async : Optional[AsyncLoggerTemplate]) -> None:
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
        self.logger_async_ : bool = logger_async
        self.logger_instance_ : Optional[LoggerTemplate] = logger_instance
        self.logger_instance_async_ : Optional[AsyncLoggerTemplate] = logger_instance_async

    def LoadData(self) -> None:
        """
        Load the data for training the model.

        Example:
        >>> param : TrainObject = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train : AnomalibTrain = AnomalibTrain(param=param, model_type_flag=model_type_flag)
        >>> anomalib_train.LoadData()
        """
        assert self.logger_async_ == False, "LoadData is not async"
        assert self.logger_instance_ is not None, "Logger instance is not set"
        self.logger_instance_.Output(text="Loading Data")

        self.dataset_unit_.AnomalibLoadFolder(
            root_path=self.param_.path_.root_, 
            normal_path=self.param_.path_.train_, 
            normal_test_path=self.param_.path_.test_good_, 
            abnormal_path=self.param_.path_.test_defective_, 
            normal_split_ratio=0.0, 
            test_split_ratio=0.0, 
            datalib_name=self.param_.name_, 
            size=self.param_.size_, 
            task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_.value)
        self.dataset_unit_.AnomalibDatasetValidation()

        self.logger_instance_.Output(text="Data Loaded")

    async def LoadDataAsync(self) -> None:
        """
        Load the data for training the model asynchronously.

        Example:
        >>> param : TrainObject = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train : AnomalibTrain = AnomalibTrain(param=param, model_type_flag=model_type_flag)
        >>> await anomalib_train.LoadDataAsync()
        """
        assert self.logger_async_ == True, "LoadDataAsync is not async"
        assert self.logger_instance_async_ is not None, "Logger instance is not set"
        await self.logger_instance_async_.Output(text="Loading Data")

        self.dataset_unit_.AnomalibLoadFolder(
            root_path=self.param_.path_.root_, 
            normal_path=self.param_.path_.train_, 
            normal_test_path=self.param_.path_.test_good_, 
            abnormal_path=self.param_.path_.test_defective_, 
            normal_split_ratio=0.0, 
            test_split_ratio=0.0, 
            datalib_name=self.param_.name_, 
            size=self.param_.size_, 
            task=AnomalyModelUnit.AnomalibTaskTypeEnum.classification_.value)
        self.dataset_unit_.AnomalibDatasetValidation()

        await self.logger_instance_async_.Output(text="Data Loaded")

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
        assert  self.logger_async_ == False, "Run is not async"
        assert self.logger_instance_ is not None, "Logger instance is not set"

        self.LoadData()

        for model_type in self.model_type_flag_:
            try:
                self.logger_instance_.Output(text=f"Training {self.param_.name_} on {model_type.value} model")
                result = self.TrainTestSequence(model_type=model_type)
                self.logger_instance_.Output(text=f"Result")
                for key, value in result[0].items():
                    self.logger_instance_.Output(text=f"{key}: {value}")
            except Exception as e:
                self.logger_instance_.Output(text=f"Error training for {self.param_.name_} on {model_type.value} model: {e}")
            continue
        self.logger_instance_.Close()

    async def RunAsync(self) -> None:
        """
        Run the training sequence asynchronously.

        Example:
        >>> param : TrainObject = TrainObject(path_=TrainPathObject(root_='root_path', train_='train_path', test_good_='test_good_path', test_defective_='test_defective_path', model_save_='model_save_path'), name_='dataset_name', size_=Size(width=256, height=256))
        >>> model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.patchcore_
        >>> anomalib_train : AnomalibTrain = AnomalibTrain(param=param, model_type_flag=model_type_flag)
        >>> await anomalib_train.RunAsync()
        """
        assert  self.logger_async_ == True, "RunAsync is not async"
        assert self.logger_instance_async_ is not None, "Logger instance is not set"

        await self.LoadDataAsync()

        for model_type in self.model_type_flag_:
            try:
                await self.logger_instance_async_.Output(text=f"Training {self.param_.name_} on {model_type.value} model")
                result = self.TrainTestSequence(model_type=model_type)
                await self.logger_instance_async_.Output(text=f"Result")
                for key, value in result[0].items():
                    await self.logger_instance_async_.Output(text=f"{key}: {value}")
            except Exception as e:
                await self.logger_instance_async_.Output(text=f"Error training for {self.param_.name_} on {model_type.value} model: {e}")
            continue
        await self.logger_instance_async_.Close()

class AnomalibTest:
    """
    The AnomalibTest class is used to test the model for the Anomalib library.

    Unimplemented as of now.
    """

    def __init__(self) -> None:
        ...

def RunModel(model_type_flag : AnomalyModelUnit.ModelTypeFlag, logger_instance : Optional[LoggerTemplate], name : str) -> None:
    """
    Allow the model to run as a package.

    NOTE : The train_object is controlled by the config file
    TODO : Build a config module for selecting the dataset
    """
    train_object : TrainObject = TrainObject(
        path=TrainPathObject(
            root='datasets/re_plant', 
            train=['train/60', 'train/top'], 
            test_good=['good/60', 'good/top'], 
            test_defective=['bad/60', "bad/top"], 
            model_save='models'
        ), 
        name=name, 
        size=Size(width=256, height=256), 
        colour_mode=ImageUnit.ColorModeEnum.rgb_
    )
    if logger_instance is None:
        anomalib_train : AnomalibTrain = AnomalibTrain(param=train_object, model_type_flag=model_type_flag, logger_async=False, logger_instance=LoggerTemplate(), logger_instance_async=None)
    else:
        anomalib_train = AnomalibTrain(param=train_object, model_type_flag=model_type_flag, logger_async=False, logger_instance=logger_instance, logger_instance_async=None)
    anomalib_train.Run()

async def RunModelAsync(model_type_flag : AnomalyModelUnit.ModelTypeFlag, logger_instance_async : Optional[AsyncLoggerTemplate], name : str) -> None:
    """
    Allow the model to run as a package asynchronously.

    NOTE : The train_object is controlled by the config file
    TODO : Build a config module for selecting the dataset
    """
    train_object : TrainObject = TrainObject(
        path=TrainPathObject(
            root='datasets/re_plant', 
            train=['train/60', 'train/top'], 
            test_good=['good/60', 'good/top'], 
            test_defective=['bad/60', "bad/top"], 
            model_save='models'
        ), 
        name=name, 
        size=Size(width=256, height=256), 
        colour_mode=ImageUnit.ColorModeEnum.rgb_
    )
    if logger_instance_async is None:
        anomalib_train : AnomalibTrain = AnomalibTrain(param=train_object, model_type_flag=model_type_flag, logger_async=True, logger_instance=None, logger_instance_async=AsyncLoggerTemplate())
    else:
        if type(logger_instance_async) == LoggerDiscord:
            assert isinstance(logger_instance_async, LoggerDiscord), "logger_instance_async is not LoggerDiscord"
            for retry in range(1,4):
                if logger_instance_async.thread_ is not None:
                    await logger_instance_async.Output(text=f"Thread retry {retry}")
                    break
                else:
                    await sleep(1)

        anomalib_train = AnomalibTrain(param=train_object, model_type_flag=model_type_flag, logger_async=True, logger_instance=None, logger_instance_async=logger_instance_async)
    await anomalib_train.RunAsync()

def main():
    """
    Run the model directly on this file.
    """
    train_object : TrainObject = TrainObject(
        path=TrainPathObject(
            root='datasets/re_plant', 
            train=['train/60', 'train/top'], 
            test_good=['good/60', 'good/top'], 
            test_defective=['bad/60', "bad/top"], 
            model_save='models'
        ), 
        name='plant_test_run', 
        size=Size(width=256, height=256), 
        colour_mode=ImageUnit.ColorModeEnum.rgb_
    )
    model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_# | AnomalyModelUnit.ModelTypeFlag.patchcore_    
    anomalib_train : AnomalibTrain = AnomalibTrain(param=train_object, model_type_flag=model_type_flag, logger_async=False, logger_instance=LoggerTemplate(), logger_instance_async=None)
    anomalib_train.Run()

if __name__ == "__main__":
    main()