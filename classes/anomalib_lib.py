from enum import Enum, unique
from typing import Optional, Final
from pandas import DataFrame

from anomalib.models.components import AnomalyModule
from anomalib.models import AiVad, Cfa, Cflow, Csflow, Draem, Dfkde, Dfm, Dsr, EfficientAd, Fastflow, Fre, Ganomaly, Padim, Patchcore, ReverseDistillation, Rkde, Stfpm, Uflow, VlmAd, WinClip, get_available_models
from anomalib.engine import Engine
from anomalib import TaskType, LearningType
from anomalib.loggers import AnomalibCometLogger, AnomalibMLFlowLogger, AnomalibTensorBoardLogger, AnomalibWandbLogger

from torch.utils.data import DataLoader, TensorDataset
from torch import tensor, float32, Tensor, device
from torch.cuda import is_available
from optuna import Trial, create_study, Study

from classes.util_lib import Deprecated

class AnomalyModelUnit: 
    """
    Class for anomaly detection model unit.
    Each model will be trained using the dataset and the model will be saved.

    Enum:
        AnomalyModelTypeEnum : Enum for different types of anomaly detection models.
        AnomalibLoggerTypeEnum : Enum for different types of logger for anomaly detection models.
    
    Dictionary:
        VALID_MODELS_DICT : Dictionary for valid models.

    Attributes:
        model_ : AnomalyModule | None : Model for anomaly detection.
        batch_size_ : int | None : Batch size for training.
        epochs_ : int | None : Number of epochs for training.
        learning_rate_ : float | None : Learning rate for training.
        threshold_ : float | None : Threshold for anomaly detection.

    Methods:
        Setter : Set the model parameters.
        ClassValidation : Validate the class parameters.
        Train : Train the model using the dataset.

    :example:
    >>> model = AnomalyModelUnit(model=AnomalyModelType.ganomaly_, batch_size=32, epochs=100, learning_rate=0.001, threshold=0.5)
    """

    @unique
    class AnomalyModelTypeEnum(Enum):
        """
        Enum for different types of anomaly detection models.

        Model from Anomalib
        AI_VAD : AI Video Anomaly Detection
        CFA : Contextual Feature Anomaly
        CFLOW : Contextual Flow Anomaly
        CSFLOW : Contextual Spatial Flow Anomaly
        DRAEM : Deep Recurrent Autoencoder for Extreme Multiclass
        DFKDE : Deep Feature Kernel Density Estimation
        DFM : Deep Feature Matching
        DSR : Deep Spatial Regression
        EFFICIENT_AD : Efficient Anomaly Detection
        FASTFLOW : Fast Flow Anomaly
        FRE : Feature Representation Ensemble
        GANOMALY : GANomaly
        PADIM : Patch-based Anomaly Detection with Image Matching
        PATCHCORE : PatchCore
        REVERSE_DISTILLATION : Reverse Distillation
        RKDE : Robust Kernel Density Estimation
        STFPM : Spatial-Temporal Feature Pyramid Matching
        UFLOW : Unsupervised Flow Anomaly Detection
        VLM_AD : Video-Level Model for Anomaly Detection
        WIN_CLIP : Windowed Clip Anomaly
        """
        ai_vad_ = AiVad
        cfa_ = Cfa
        cflow_ = Cflow
        csflow_ = Csflow
        draem_ = Draem # can or cannot be used
        dfkde_ = Dfkde
        dfm_ = Dfm
        dsr_ = Dsr
        efficient_ad_ = EfficientAd
        fastflow_ = Fastflow
        fre_ = Fre
        ganomaly_ = Ganomaly
        padim_ = Padim
        patchcore_ = Patchcore
        reverse_distillation_ = ReverseDistillation
        rkde_ = Rkde
        stfpm_ = Stfpm
        uflow_ = Uflow
        vlm_ad_ = VlmAd
        win_clip_ = WinClip


    VALID_MODELS_DICT: Final[dict[AnomalyModelTypeEnum, bool]] = {
        AnomalyModelTypeEnum.ai_vad_ : False,
        AnomalyModelTypeEnum.cfa_ : False,
        AnomalyModelTypeEnum.cflow_ : False,
        AnomalyModelTypeEnum.csflow_ : False,
        AnomalyModelTypeEnum.draem_ : True,
        AnomalyModelTypeEnum.dfkde_ : True,
        AnomalyModelTypeEnum.dfm_ : False,
        AnomalyModelTypeEnum.dsr_ : False,
        AnomalyModelTypeEnum.efficient_ad_ : False,
        AnomalyModelTypeEnum.fastflow_ : True,
        AnomalyModelTypeEnum.fre_ : False,
        AnomalyModelTypeEnum.ganomaly_ : True,
        AnomalyModelTypeEnum.padim_ : True,
        AnomalyModelTypeEnum.patchcore_ : True,
        AnomalyModelTypeEnum.reverse_distillation_ : True,
        AnomalyModelTypeEnum.rkde_ : False,
        AnomalyModelTypeEnum.stfpm_ : True,
        AnomalyModelTypeEnum.uflow_ : False,
        AnomalyModelTypeEnum.vlm_ad_ : False,
        AnomalyModelTypeEnum.win_clip_ : False
    }

    @unique
    class AnomalibLoggerTypeEnum(Enum):
        """
        Enum for different types of logger for anomaly detection models.

        Logger from Anomalib
        COMET : Comet Logger
        MLFLOW : MLFlow Logger
        TENSORBOARD : TensorBoard Logger
        WANDB : Wandb Logger
        """
        comet_ = AnomalibCometLogger
        mlflow_ = AnomalibMLFlowLogger
        tensorboard_ = AnomalibTensorBoardLogger
        wandb_ = AnomalibWandbLogger
        none_ = None

    @unique
    class AnomalibTaskTypeEnum(Enum):   
        """
        Enum for different types of task for anomaly detection models.

        Task from Anomalib
        CLASSIFICATION : Classification Task
        DETECTION : Detection Task
        SEGMENTATION : Segmentation Task
        """
        classification_ = TaskType.CLASSIFICATION
        detection_ = TaskType.DETECTION
        segmentation_ = TaskType.SEGMENTATION

    @unique
    class AnomalibLearningTypeEnum(Enum):
        """
        Enum for different types of learning for anomaly detection models.

        Learning from Anomalib
        ONE_CLASS : One Class Learning
        ZERO_SHOT : Zero Shot Learning
        FEW_SHOT : Few Shot Learning
        """
        one_class_ = LearningType.ONE_CLASS
        zero_shot_ = LearningType.ZERO_SHOT
        few_shot_ = LearningType.FEW_SHOT


    def __init__(self, *, model_type : Optional[AnomalyModelTypeEnum] = None, batch_size : Optional[int] = None, epochs : Optional[int] = None, learning_rate : Optional[float] = None, threshold : Optional[float] = None) -> None:
        """
        Initialize the model.

        Args:
            model : (Optional[AnomalyModule]) : Model for anomaly detection. Default is None.
            batch_size : (Optional[int]) : Batch size for training. Default is None.
            epochs : (Optional[int]) : Number of epochs for training. Default is None.
            learning_rate : (Optional[float]) : Learning rate for training. Default is None.
            threshold : (Optional[float]) : Threshold for anomaly detection. Default is None.
        """
        self.model_ : Optional[AnomalyModule] = None
        self.engine_ : Optional[Engine] = None
        self.model_type_ : Optional[AnomalyModelUnit.AnomalyModelTypeEnum] = model_type
        self.batch_size_ : Optional[int] = batch_size
        self.epochs_ : Optional[int] = epochs
        self.learning_rate_ : Optional[float] = learning_rate
        self.threshold_ : Optional[float] = threshold

    def Setter(self, *, model_type : Optional[AnomalyModelTypeEnum] = None, batch_size : Optional[int] = None, epochs : Optional[int] = None, learning_rate : Optional[float] = None, threshold : Optional[float] = None) -> None:
        """
        Set the model parameters.

        Args:
            model : (Optional[AnomalyModule]) : Model for anomaly detection. Default is None.
            batch_size : (Optional[int]) : Batch size for training. Default is None.
            epochs : (Optional[int]) : Number of epochs for training. Default is None.
            learning_rate : (Optional[float]) : Learning rate for training. Default is None.
            threshold : (Optional[float]) : Threshold for anomaly detection. Default is None.

        :example:
        >>> model = AnomalyModelUnit()
        >>> model.Setter(model=AnomalyModelType.ganomaly_, batch_size=32, epochs=100, learning_rate=0.001, threshold=0.5)
        """
        if model_type is not None:
            self.model_type_ = model_type
        if batch_size is not None:
            self.batch_size_ = batch_size
        if epochs is not None:
            self.epochs_ = epochs
        if learning_rate is not None:
            self.learning_rate_ = learning_rate
        if threshold is not None:
            self.threshold_ = threshold

    def ClassValidation(self) -> None:
        """
        Validate the class parameters.

        :example:
        >>> model = AnomalyModelUnit()
        >>> model.Setter(model=AnomalyModelType.ganomaly_, batch_size=32, epochs=100, learning_rate=0.001, threshold=0.5)
        >>> model.ClassValidation() # No assertion error
        """
        assert self.model_type_ is not None, "Model must be set"
        assert self.batch_size_ is not None, "Batch Size must be set"
        assert self.epochs_ is not None, "Epochs must be set"
        assert self.learning_rate_ is not None, "Learning Rate must be set"
        assert self.threshold_ is not None, "Threshold must be set"

    def Train(self, *, dataset : DataFrame, logger : AnomalibLoggerTypeEnum, task_type : AnomalibTaskTypeEnum) -> None:
        # This function will implement the training of the model for any model type 
        """
        TODO: Write this later
        """
        
        self.ClassValidation()
        assert self.model_type_ is not None, "Typechecking failed"

        self.model_ = self.model_type_.value()
        assert isinstance(self.model_, self.model_type_.value), "Model is not of the correct type"

        print(self.model_.learning_type) # This should print the learning type of the model



@Deprecated("This function is deprecated. Use Enum AnomalyModelType instead.")
def GetModel() -> list[str]:
    """
    Deprecated: Returns the list of available anomaly detection models.
    
    Use Enum AnomalyModelType instead.
    """
    return list(get_available_models())
