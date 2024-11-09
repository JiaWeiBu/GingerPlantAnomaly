# Import only the function needed
from enum import Enum, unique
from typing import Any
from pandas import DataFrame, concat
from pycaret.anomaly import setup, create_model, save_model, load_model, evaluate_model, predict_model, plot_model#, get_config, set_config # type: ignore
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score # type: ignore

from classes.util_lib import Unused

# Base class for anomaly detection models
class PyCaretModelUnit :
    """
    Class for anomaly detection model unit.
    This is for the traditional method of anomaly detection using PyCaret library.

    Attributes:
        model_ : Internal Pycaret setup model. (Pycaret will handle the model)
    
    Methods:
        Train : Train the model using the dataset.
        Evaluate : Evaluate the model.
        Predict : Predict anomalies in the dataset.
        Results : Save the prediction results to a CSV file.
        EvaluationMetrics : Evaluate the model using the test data.
        Plot : Plot the model.
        Save : Save the model.

    :example:
    >>> model = PyCaretModelUnit()
    >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
    >>> model.Evaluate()
    >>> model.Predict(test)
    >>> model.Results(test, "test")
    >>> model.Save("knn_model")
    """

    @unique
    class PyCaretModelTypeEnum(Enum):
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
        #mcd_ = "mcd"

    # class ModelSourceEnum(Enum):
    #     """
    #     Enum for different sources of anomaly detection models.

    #     Model from Pycaret
    #     PYCARET : Pycaret library
    #     CUSTOM : Custom implementation
    #     """
    #     pycaret_ = 1
    #     custom_ = 2

    class PyCaretPlotTypeEnum(Enum):
        """
        Enum for different types of plots for anomaly detection models.

        Plot from Pycaret
        TSNE : t-Distributed Stochastic Neighbor Embedding
        UMAP : Uniform Manifold Approximation and Projection
        """
        tsne_ = "tsne"
        umap_ = "umap"


    def __init__(self) -> None:
        """
        Initialize the model. 
        """
        self.model_ : Any = None

    def Train(self, *, data : DataFrame, model_type : PyCaretModelTypeEnum, model_path = None) -> None:
        """
        Train the model using the dataset.

        Args:
            data : DataFrame : Dataset for training the model.
            model_type : PyCaretModelType : Type of model to train.
            model_path : str : Path to the model to load. Default is None.

        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        """
        exp : Any = setup(data=data, use_gpu=True, normalize_method="minmax", normalize=True)
        Unused(exp)
        
        if model_path is None:
            self.model_ = create_model(model_type.value)
        else:
            self.model_ = create_model(load_model("./model/"+model_path))

    def Evaluate(self) -> None:
        """
        Evaluate the model.

        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Evaluate()
        """
        evaluate_model(model=self.model_)

    def Predict(self, data : DataFrame) -> DataFrame:
        """
        Predict anomalies in the dataset.

        Args:
            data : DataFrame : Dataset for predicting anomalies.
        
        Returns:
            DataFrame : Predicted anomalies in the dataset.
        
        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Predict(test)
        """
        return predict_model(model=self.model_, data=data)

    def Results(self, data : DataFrame, name : str) -> None:
        """
        Save the prediction results to a CSV file.

        Args:
            data : DataFrame : Dataset for saving the prediction results.
            name : str : Name of the CSV file to save the results.
        
        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Results(test, "test")
        """
        # Save prediction of last 2 columns
        predictions : DataFrame = self.Predict(data).iloc[:, -2:]
        predictions.to_csv('./results/'+name+'.csv')
        print("Results saved at ./results/"+name+".csv")

    def EvaluationMetrics(self, good : DataFrame, defective : DataFrame, name : str) -> None:
        """
        Evaluate the model using the test data.

        Args:
            good : DataFrame : Good test data for evaluation.
            defective : DataFrame : Defective test data for evaluation.
            name : str : Name of the model for evaluation.
        
        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.EvaluationMetrics(test_good, test_defective, "knn_model")
        """
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

        with open('./results/result.csv', 'a', encoding='utf-8') as f:
            f.write(f"{name},{accuracy},{precision},{recall},{f1}\n")

    def Plot(self, plot_type : PyCaretPlotTypeEnum) -> None:
        """
        Plot the model.

        Args:
            plot_type : PyCaretPlotType : Type of plot to display.
        
        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Plot(PyCaretPlotType.tsne_)
        """
        plot_model(model=self.model_, plot=plot_type.value)

    def Save(self, model_name : str) -> None:
        """
        Save the model.

        Args:
            model_name : str : Name of the model to save.

        :example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Save("knn_model")
        """
        save_model(self.model_, "./model/"+model_name)

    # def GetConfig(self) -> dict:
    #     return get_config()

    # def SetConfig(self, config : dict) -> None:
    #     set_config(config)
