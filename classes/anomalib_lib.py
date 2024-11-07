# anomalib library
# This library contains the functions that are used to detect anomalies in the data

from anomalib import models
from enum import Enum, unique
from pandas import DataFrame
from classes.utility import Deprecated

@unique
class AnomalyModelType(Enum):
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
    #ai_vad_ = "ai_vad"
    #cfa_ = "cfa"
    #cflow_ = "cflow"
    #csflow_ = "csflow"
    #draem_ = "draem" can or cannot
    dfkde_ = "dfkde"
    #dfm_ = "dfm"
    #dsr_ = "dsr"
    #efficient_ad_ = "efficient_ad"
    fastflow_ = "fastflow"
    #fre_ = "fre"
    ganomaly_ = "ganomaly"
    padim_ = "padim"
    patchcore_ = "patchcore"
    reverse_distillation_ = "reverse_distillation"
    #rkde_ = "rkde"
    stfpm_ = "stfpm"
    #uflow_ = "uflow"
    #vlm_ad_ = "vlm_ad"
    #win_clip_ = "win_clip"


class AnomalyModelUnit: 
    def __init__(self, batch_size : int | None = None, epochs : int | None = None, learning_rate : float | None = None, threshold : float | None = None) -> None:
        self.model_ = None
        self.batach_size_ : int | None = batch_size
        self.epochs_ : int | None = epochs
        self.learning_rate_ : float | None = learning_rate
        self.threshold_ : float | None = threshold

    def Setter(self, *, batch_size : int | None = None, epochs : int | None = None, learning_rate : float | None = None, threshold : float | None = None) -> None:
        if batch_size:
            self.batch_size_ = batch_size
        if epochs:
            self.epochs_ = epochs
        if learning_rate:
            self.learning_rate_ = learning_rate
        if threshold:
            self.threshold_ = threshold

    def ClassValidation(self) -> None:
        assert self.batch_size_ is not None, "Batch Size must be set"
        assert self.epochs_ is not None, "Epochs must be set"
        assert self.learning_rate_ is not None, "Learning Rate must be set"
        assert self.threshold_ is not None, "Threshold must be set"

    def Train(self, *, dataset : DataFrame, model_type : AnomalyModelType) -> None:
        self.model_ = models.get_model(model_type.value)
        self.model_.train(dataset)

@Deprecated("This function is deprecated. Use Enum AnomalyModelType instead.")
def GetModel() -> list[str]:
    """
    Deprecated: Returns the list of available anomaly detection models.
    
    Use Enum AnomalyModelType instead.
    """
    return list(models.get_available_models())
