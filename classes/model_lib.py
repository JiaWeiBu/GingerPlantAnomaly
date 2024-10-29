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
from pandas import DataFrame, concat
from pycaret.anomaly import setup, create_model, save_model, load_model, evaluate_model, predict_model, plot_model # type: ignore
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score # type: ignore

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
    abod_ = "abod"
    cluster_ = "cluster"
    cof_ = "cof"
    histogram_ = "histogram"
    iforest_ = "iforest"
    knn_ = "knn"
    lof_ = "lof"
    svm_ = "svm"
    pca_ = "pca"
    sod_ = "sod"
    sos_ = "sos"
    mcd_ = "mcd"

class ModelSource(Enum):
    """
    Enum for different sources of anomaly detection models.

    Model from Pycaret
    PYCARET : Pycaret library
    CUSTOM : Custom implementation
    """
    pycaret_ = 1
    custom_ = 2

class PlotType(Enum):
    """
    Enum for different types of plots for anomaly detection models.

    Plot from Pycaret
    TSNE : t-Distributed Stochastic Neighbor Embedding
    UMAP : Uniform Manifold Approximation and Projection
    """
    tsne_ = "tsne"
    umap_ = "umap"

# Base class for anomaly detection models
class ModelUnit :
    def __init__(self) -> None:
        self.model_ = None

    def Train(self, *, data : DataFrame, model_type : ModelType, model_path = None) -> None:
        exp = setup(data=data, use_gpu=True, normalize_method="minmax", normalize=True)
        
        if model_path is None:
            self.model_ = create_model(model_type.value)
        else:
            self.model_ = create_model(load_model("./model/"+model_path))

    def Evaluate(self) -> None:
        evaluate_model(model=self.model_)

    def Predict(self, data : DataFrame) -> DataFrame:
        return predict_model(model=self.model_, data=data)

    def Results(self, data : DataFrame, name : str) -> None:
        # Save prediction of last 2 columns
        predictions = self.Predict(data).iloc[:, -2:]
        predictions.to_csv('./results/'+name+'.csv')
        print("Results saved at ./results/"+name+".csv")

    def EvaluationMetrics(self, good : DataFrame, defective : DataFrame, name : str) -> None:
        good_predictions = DataFrame(self.Predict(good)["Anomaly"])
        defective_predictions = DataFrame(self.Predict(defective)["Anomaly"])

        # insert another column called "label" to indicate good or defective
        good_predictions["label"] = 0
        defective_predictions["label"] = 1

        # combine good and defective predictions
        result = concat([good_predictions, defective_predictions])

        result.to_csv('./results/'+name+'.csv')

        # accuracy, percision, recall, f1-score
        accuracy = accuracy_score(result["label"], result["Anomaly"])
        precision = precision_score(result["label"], result["Anomaly"])
        recall = recall_score(result["label"], result["Anomaly"])
        f1 = f1_score(result["label"], result["Anomaly"])

        print(name, "result")
        print("Accuracy : ", accuracy)
        print("Precision : ", precision)
        print("Recall : ", recall)
        print("F1-score : ", f1)

        with open('./results/result.csv', 'a') as f:
            f.write(f"{name},{accuracy},{precision},{recall},{f1}\n")

    def Plot(self, plot_type : PlotType) -> None:
        plot_model(model=self.model_, plot=plot_type.value)

    def Save(self, model_name : str) -> None:
        save_model(self.model_, "./model/"+model_name)

    


        



    