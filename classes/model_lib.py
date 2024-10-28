# This file defines the core structure for anomaly detection models, introducing a base class `AnomalyModel`.
# All custom anomaly detection models should inherit from this base class, ensuring a consistent interface
# for anomaly detection across different implementations. By defining a superclass with essential methods
# for model training, evaluation, and anomaly prediction, this structure allows for streamlined integration
# and extendability of various anomaly detection models within the system.
"""
Class : Model
Purpose : A superclass providing a framework for implementing various anomaly detection models. 
          It enforces a standard method interface that all derived classes should follow, ensuring
          consistency in training, predicting, and evaluating anomalies.

Methods :
  - __init__ : Initializes model parameters and configurations.
  - train : Abstract method intended for training the model; must be overridden in subclasses.
  - predict : Abstract method for detecting anomalies; implemented uniquely in each subclass.
  - evaluate : Abstract method for evaluating model performance on test data.

Note :
This is library code, all external code will be linked with a facade layer

Variables naming convention
- GLOBAL_VARIABLE 
- class_variable_
- ClassName
- variable_name
- k_constant_variable
- FunctionName
"""

# Import only the function needed
from enum import Enum, unique


# Enum
@unique
class ModelType(Enum):
    """
    Enum for different types of anomaly detection models.

    Model from Pycaret
    ABOD : Angle-base Outlier Detection
    CLUSTER : Clustering-Based Local Outlier
    COF : Connectivity-Based Outlier Factor
    HISTOGRAM : Histogram-based Outlier Detection
    IFOREST : Isolation Forest
    KNN : k-Nearest Neighbors Detector
    LOF : Local Outlier Factor
    SVM : One-class SVM detector
    PCA : Principal Component Analysis
    MCD : Minimum Covariance Determinant
    SOD : Subspace Outlier Detection
    SOS : Stochastic Outlier Selection
    """
    ABOD = "abod"
    CLUSTER = "cluster"
    COF = "cof"
    HISTOGRAM = "histogram"
    IFOREST = "iforest"
    KNN = "knn"
    LOF = "lof"
    SVM = "svm"
    PCA = "pca"
    MCD = "mcd"
    SOD = "sod"
    SOS = "sos"

class ModelSource(Enum):
    """
    Enum for different sources of anomaly detection models.

    Model from Pycaret
    PYCARET : Pycaret library
    CUSTOM : Custom implementation
    """
    PYCARET = 1
    CUSTOM = 2

# Base class for anomaly detection models
class Model:
    def __init__(self, model_source : ModelSource, model_name : str, model_type : ModelType):
        self.model_source : ModelSource = model_source
        self.model_name : str = model_name
        self.model_type : ModelType = model_type

    def Predict(self, data):
        raise NotImplementedError("Subclasses must implement this method.")
    