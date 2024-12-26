# Import only the function needed
from enum import Flag, auto
from typing import Any, Final
from pandas import DataFrame, concat
from pycaret.anomaly import setup, create_model, save_model, load_model, evaluate_model, predict_model, plot_model#, get_config, set_config # type: ignore
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score # type: ignore

from classes.util_lib import Unused

# Base class for anomaly detection models
class PyCaretModelUnit :
    """
    Class for anomaly detection model unit.
    This is for the traditional method of anomaly detection using PyCaret library.

    Flags:
    ModelTypeFlag : Flag for different types of anomaly detection models.
    PlotTypeFlag : Flag for different types of plots for anomaly detection models.

    Attributes:
    model_ : Internal Pycaret setup model. (Pycaret will handle the model)
    ModelTypeFlagName : dict[PyCaretModelType, str] : Dictionary for model type flag and name.
    PlotTypeFlagName : dict[PyCaretPlotType, str] : Dictionary for plot type flag and name.

    Methods:
    Train : Train the model using the dataset.
    Evaluate : Evaluate the model.
    Predict : Predict anomalies in the dataset.
    Results : Save the prediction results to a CSV file.
    EvaluationMetrics : Evaluate the model using the test data.
    Plot : Plot the model.
    Save : Save the model.

    Example:
    >>> model = PyCaretModelUnit()
    >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
    >>> model.Evaluate()
    >>> model.Predict(test)
    >>> model.Results(test, "test")
    >>> model.Save("knn_model")
    """

    class ModelTypeFlag(Flag):
        """
        Flag for different types of anomaly detection models.

        Attributes:
        abod_ : Angle-base Outlier Detection
        cluster_ : Clustering-Based Local Outlier
        cof_ : Connectivity-Based Outlier Factor
        histogram_ : Histogram-based Outlier Detection
        iforest_ : Isolation Forest
        knn_ : k-Nearest Neighbors Detector
        lof_ : Local Outlier Factor
        svm_ : One-class SVM detector
        pca_ : Principal Component Analysis
        mcd_ : Minimum Covariance Determinant
        sod_ : Subspace Outlier Detection
        sos_ : Stochastic Outlier Selection
        optimal_ : Optimal model for anomaly detection (All models except MCD)

        Example:
        >>> model = PyCaretModelUnit()
        >>> # Train using IFOREST, KNN and SVM
        >>> model_train = PyCaretModelType.IFOREST | PyCaretModelType.KNN | PyCaretModelType.SVM
        >>> for model_type in model_train:
        >>>     model.Train(data=train, model_type=model_type)
        """
        abod_ = auto()
        cluster_ = auto()
        cof_ = auto()
        histogram_ = auto()
        iforest_ = auto()
        knn_ = auto()
        lof_ = auto()
        svm_ = auto()
        pca_ = auto()
        mcd_ = auto()
        sod_ = auto()
        sos_ = auto()
        optimal_ = abod_ | cluster_ | cof_ | histogram_ | iforest_ | knn_ | lof_ | svm_ | pca_ | sod_ | sos_

    ModelTypeFlagName : Final[dict[ModelTypeFlag, str]] = {
        ModelTypeFlag.abod_ : "abod",
        ModelTypeFlag.cluster_ : "cluster",
        ModelTypeFlag.cof_ : "cof",
        ModelTypeFlag.histogram_ : "histogram",
        ModelTypeFlag.iforest_ : "iforest",
        ModelTypeFlag.knn_ : "knn",
        ModelTypeFlag.lof_ : "lof",
        ModelTypeFlag.svm_ : "svm",
        ModelTypeFlag.pca_ : "pca",
        ModelTypeFlag.sod_ : "sod",
        ModelTypeFlag.sos_ : "sos",
        ModelTypeFlag.mcd_ : "mcd",
    }

    # class ModelSourceEnum(Enum):
    #     """
    #     Enum for different sources of anomaly detection models.

    #     Model from Pycaret
    #     PYCARET : Pycaret library
    #     CUSTOM : Custom implementation
    #     """
    #     pycaret_ = 1
    #     custom_ = 2

    class PlotTypeFlag(Flag):
        """
        Enum for different types of plots for anomaly detection models.

        Attributes:
        tsne_ : t-Distributed Stochastic Neighbor Embedding
        umap_ : Uniform Manifold Approximation and Projection

        Example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Plot(PyCaretPlotType.tsne_)
        """
        tsne_ = auto()
        umap_ = auto()

    PlotTypeFlagName : Final[dict[PlotTypeFlag, str]] = {
        PlotTypeFlag.tsne_ : "tsne",
        PlotTypeFlag.umap_ : "umap",
    }

    def __init__(self) -> None:
        """
        Initialize the model. 

        Attributes:
        model_ : Any : Internal Pycaret setup model. (Pycaret will handle the model)

        Example:
        >>> model = PyCaretModelUnit()
        """
        self.model_ : Any = None

    def Train(self, *, data : DataFrame, model_type : ModelTypeFlag, model_path = None) -> None:
        """
        Train the model using the dataset.

        Args:
        data : DataFrame : Dataset for training the model.
        model_type : PyCaretModelType : Type of model to train.
        model_path : str : Path to the model to load. Default is None.

        Example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        """
        exp : Any = setup(data=data, use_gpu=True, normalize_method="minmax", normalize=True)
        Unused(exp)
        
        if model_path is None:
            if model_type in self.ModelTypeFlagName:
                self.model_ = create_model(self.ModelTypeFlagName[model_type])
            else:
                raise ValueError("Single model type only, no combination")
        else:
            self.model_ = create_model(load_model(model_path))

    def Evaluate(self) -> None:
        """
        Evaluate the model.

        Example:
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
        
        Example:
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
        
        Example:
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
        
        Example:
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
        roc_auc = roc_auc_score(result["label"], result["Anomaly"])

        print(name, "result")
        print("Accuracy : ", accuracy)
        print("Precision : ", precision)
        print("Recall : ", recall)
        print("F1-score : ", f1)
        print("AUROC : ", roc_auc)

        with open('./results/result.csv', 'a', encoding='utf-8') as f:
            f.write(f"{name},{accuracy},{precision},{recall},{f1},{roc_auc}\n")

    def Plot(self, plot_type : PlotTypeFlag) -> None:
        """
        Plot the model.

        Args:
        plot_type : PyCaretPlotType : Type of plot to display.
        
        Example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Plot(PyCaretPlotType.tsne_)
        """
        plot_model(model=self.model_, plot=self.PlotTypeFlagName[plot_type])

    def Save(self, model_name : str) -> None:
        """
        Save the model.

        Args:
        model_name : str : Name of the model to save.

        Example:
        >>> model = PyCaretModelUnit()
        >>> model.Train(data=train, model_type=PyCaretModelType.knn_)
        >>> model.Save("knn_model")
        """
        save_model(self.model_, "./model/"+model_name)

    # def GetConfig(self) -> dict:
    #     return get_config()

    # def SetConfig(self, config : dict) -> None:
    #     set_config(config)
