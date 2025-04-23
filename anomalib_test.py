from os.path import exists
from os import makedirs
from typing import Any, Optional
from enum import Enum, unique, auto
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size
from classes.anomalib_lib import AnomalyModelUnit
from anomalib.deploy.inferencers import TorchInferencer
from anomalib.utils.visualization.image import ImageResult
from classes.log_lib import LoggerTemplate, AsyncLoggerTemplate, LoggerWebhook
from classes.discord_lib import MessageObject

class ModelPathUnit:

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
        stpm_ = auto()



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
        week3_ = auto()
        week8_ = auto()
        week12_ = auto()
        week18_ = auto()
    
    def __init__(self) -> None:
        """
        Initialize the ModelPathUnit class.
        """
        self.model_week_dict_: dict[ModelPathUnit.ModelWeekEnum, str] = {
            ModelPathUnit.ModelWeekEnum.week3_: "3",
            ModelPathUnit.ModelWeekEnum.week8_: "8",
            ModelPathUnit.ModelWeekEnum.week12_: "12",
            ModelPathUnit.ModelWeekEnum.week18_: "18",
        }


    def ModelPath(self, type: ModelTypeEnum, week: ModelWeekEnum) -> str:
        """
        Get the model path.

        Args:
        type : ModelTypeEnum - The type of the model.
        week : ModelWeekEnum - The week of the model.

        Returns:
        str - The model path.
        """
        return f"models/T5_Full_Individual_Filtered_Week_Unseen_Week{week.value}_Save_SimMutiAnomaly/{type.name}/weights/torch/model.pt"

class AnomalibTest:
    """
    The AnomalibTest class is used to test the model for the Anomalib library.

    Attributes:
    param_ : TestObject - The TestObject containing the parameters for testing the model.
    logger_async_ : bool - Indicates if the logger is asynchronous.
    logger_instance_ : Optional[LoggerTemplate] - Synchronous logger instance.
    logger_instance_async_ : Optional[AsyncLoggerTemplate] - Asynchronous logger instance.
    """

    def __init__(self, *, param: DatasetUnit, logger_async: bool, logger_instance: Optional[LoggerTemplate], logger_instance_async: Optional[AsyncLoggerTemplate]) -> None:
        """
        Initialize the AnomalibTest class.

        Args:
        param : DatasetUnit - The DatasetUnit containing the test dataset.
        logger_async : bool - Indicates if the logger is asynchronous.
        logger_instance : Optional[LoggerTemplate] - Synchronous logger instance.
        logger_instance_async : Optional[AsyncLoggerTemplate] - Asynchronous logger instance.
        """
        self.param_: DatasetUnit = param
        self.logger_async_: bool = logger_async
        self.logger_instance_: Optional[LoggerTemplate] = logger_instance
        self.logger_instance_async_: Optional[AsyncLoggerTemplate] = logger_instance_async
        self.message_object_: MessageObject = MessageObject()
    
    def Evaluate(self, *, model_path: str) -> None:
        """
        Evaluate the model on the test data.

        Args:
        model_path : str - Path to the trained model.

        Example:
        >>> test_unit = DatasetUnit()
        >>> anomalib_test = AnomalibTest(param=test_unit, logger_async=False, logger_instance=LoggerTemplate(), logger_instance_async=None)
        >>> anomalib_test.Evaluate(model_path="models/model.pt")
        """
        assert self.logger_instance_ is not None, "Logger instance is not set"
        self.logger_instance_.Output(text=f"Evaluating model at {model_path}")

        inferencer = TorchInferencer(path=model_path)
        for image in self.param_.images_:
            result: ImageResult = inferencer.predict(image)
            self.logger_instance_.Output(text=f"Prediction: {result.pred_label}")

        self.logger_instance_.Output(text="Evaluation Complete")

    async def EvaluateAsync(self, *, model_path: str) -> None:
        """
        Evaluate the model on the test data asynchronously.

        Args:
        model_path : str - Path to the trained model.

        Example:
        >>> test_unit = DatasetUnit()
        >>> anomalib_test = AnomalibTest(param=test_unit, logger_async=True, logger_instance=None, logger_instance_async=AsyncLoggerTemplate())
        >>> await anomalib_test.EvaluateAsync(model_path="models/model.pt")
        """
        assert self.logger_instance_async_ is not None, "Logger instance is not set"
        self.message_object_.SetMessage(f"Evaluating model at {model_path}")
        await self.logger_instance_async_.Output(message_object=self.message_object_)
        self.message_object_.ClearMessage()

        inferencer = TorchInferencer(path=model_path)
        for image in self.param_.images_:
            result: ImageResult = inferencer.predict(image)
            self.message_object_.SetMessage(f"Prediction: {result.pred_label}")
            await self.logger_instance_async_.Output(message_object=self.message_object_)
            self.message_object_.ClearMessage()

        self.message_object_.SetMessage("Evaluation Complete")
        await self.logger_instance_async_.Output(message_object=self.message_object_)
        self.message_object_.ClearMessage()

    def Run(self, *, model_path: str) -> None:
        """
        Run the testing sequence.

        Args:
        model_path : str - Path to the trained model.

        Example:
        >>> test_unit = DatasetUnit()
        >>> anomalib_test = AnomalibTest(param=test_unit, logger_async=False, logger_instance=LoggerTemplate(), logger_instance_async=None)
        >>> anomalib_test.Run(model_path="models/model.pt")
        """
        assert self.logger_async_ == False, "Run is not async"
        assert self.logger_instance_ is not None, "Logger instance is not set"

        self.LoadData()
        self.Evaluate(model_path=model_path)

    async def RunAsync(self, *, model_path: str) -> None:
        """
        Run the testing sequence asynchronously.

        Args:
        model_path : str - Path to the trained model.

        Example:
        >>> test_unit = DatasetUnit()
        >>> anomalib_test = AnomalibTest(param=test_unit, logger_async=True, logger_instance=None, logger_instance_async=AsyncLoggerTemplate())
        >>> await anomalib_test.RunAsync(model_path="models/model.pt")
        """
        assert self.logger_async_ == True, "RunAsync is not async"
        assert self.logger_instance_async_ is not None, "Logger instance is not set"

        await self.LoadDataAsync()
        await self.EvaluateAsync(model_path=model_path)

def main():
    """
    Run the testing sequence directly from this file.
    """
    test_unit = DatasetUnit()
    anomalib_test = AnomalibTest(
        param=test_unit,unit   loggerunit   sync=False,
        logger_instance=LoggerTemplate(),
        logger_instance_async=None
    )
    anomalib_test.Run(model_path="models/model.pt")

if __name__ == "__main__":
    main()