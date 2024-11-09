# anomalib library
# This library contains the functions that are used to detect anomalies in the data
from anomalib.models.components import AnomalyModule
from pandas import DataFrame

from classes.util_lib import Deprecated
from classes.enum import AnomalyModelType, VALID_MODELS_DICT


class AnomalyModelUnit: 
    """
    Class for anomaly detection model unit.

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

    def __init__(self, *, model : AnomalyModule | None = None, batch_size : int | None = None, epochs : int | None = None, learning_rate : float | None = None, threshold : float | None = None) -> None:
        """
        Initialize the model.

        Args:
            model : AnomalyModule | None : Model for anomaly detection. Default is None.
            batch_size : int | None : Batch size for training. Default is None.
            epochs : int | None : Number of epochs for training. Default is None.
            learning_rate : float | None : Learning rate for training. Default is None.
            threshold : float | None : Threshold for anomaly detection. Default is None.
        """
        self.model_ : AnomalyModule | None = model
        self.batach_size_ : int | None = batch_size
        self.epochs_ : int | None = epochs
        self.learning_rate_ : float | None = learning_rate
        self.threshold_ : float | None = threshold

    def Setter(self, *, model : AnomalyModule | None = None, batch_size : int | None = None, epochs : int | None = None, learning_rate : float | None = None, threshold : float | None = None) -> None:
        """
        Set the model parameters.

        Args:
            model : AnomalyModule | None : Model for anomaly detection. Default is None.
            batch_size : int | None : Batch size for training. Default is None.
            epochs : int | None : Number of epochs for training. Default is None.
            learning_rate : float | None : Learning rate for training. Default is None.
            threshold : float | None : Threshold for anomaly detection. Default is None.

        :example:
        >>> model = AnomalyModelUnit()
        >>> model.Setter(model=AnomalyModelType.ganomaly_, batch_size=32, epochs=100, learning_rate=0.001, threshold=0.5)
        """
        if model is not None:
            self.model_ = model
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
        assert self.model_ is not None, "Model must be set"
        assert self.batch_size_ is not None, "Batch Size must be set"
        assert self.epochs_ is not None, "Epochs must be set"
        assert self.learning_rate_ is not None, "Learning Rate must be set"
        assert self.threshold_ is not None, "Threshold must be set"

    def Train(self, *, dataset : DataFrame, model_type : AnomalyModelType) -> None:
        ...

@Deprecated("This function is deprecated. Use Enum AnomalyModelType instead.")
def GetModel() -> list[str]:
    """
    Deprecated: Returns the list of available anomaly detection models.
    
    Use Enum AnomalyModelType instead.
    """
    return list(models.get_available_models())
