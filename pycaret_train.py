from pandas import DataFrame
from classes.general_lib import TrainObject, TrainPathObject, PredictPathObject
from classes.pycaret_lib import PyCaretModelUnit
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size

class PycaretTrain:
    """
    Pycaret training class

    TODO: Implement Config

    Attributes:
    params_ : TrainObject - training object
    model_ : PyCaretModelUnit - model unit
    model_type_flag_ : PyCaretModelUnit.ModelTypeFlag - model type flag

    Example:
    >>> path = TrainPathObject("train", "test_good", "test_defective")
    >>> train = TrainObject(path, ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
    >>> run = RunPycaret(param=train)
    """

    def __init__(self, *, param : TrainObject, model_type_flag : PyCaretModelUnit.ModelTypeFlag = PyCaretModelUnit.ModelTypeFlag.knn_ | PyCaretModelUnit.ModelTypeFlag.iforest_):
        """
        Initialize RunPycaret

        Args:
        param : TrainObject - training object
        model_type_flag : PyCaretModelUnit.ModelTypeFlag - model type flag

        Attributes:
        params_ : TrainObject - training object
        model_ : PyCaretModelUnit - model unit
        model_type_flag_ : PyCaretModelUnit.ModelTypeFlag - model type flag

        Example:
        >>> path = TrainPathObject("train", "test_good", "test_defective")
        >>> train = TrainObject(path, ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
        >>> run = RunPycaret(param=train)
        """
        self.params_ = param
        self.model_ = PyCaretModelUnit()
        self.model_type_flag_ : PyCaretModelUnit.ModelTypeFlag = model_type_flag

    def LoadData(self) -> tuple[DataFrame, DataFrame, DataFrame]:
        """
        Load data

        Returns:
        tuple[DataFrame, DataFrame, DataFrame] - training, good test, and defective test data

        Example:
        >>> path = TrainPathObject("train", "test_good", "test_defective")
        >>> train = TrainObject(path, ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
        >>> run = RunPycaret(param=train)
        >>> train, test_good, test_defective = run.LoadData()
        """
        print("Loading Data")

        train_module = DatasetUnit()
        train_module.LoadImagesResize(f"{self.params_.path_.root_}/{self.params_.path_.train_}", self.params_.colour_mode_, self.params_.size_)

        test_good_module = DatasetUnit()
        test_good_module.LoadImagesResize(f"{self.params_.path_.root_}/{self.params_.path_.test_good_}", self.params_.colour_mode_, self.params_.size_)
        
        test_defective_module = DatasetUnit()
        test_defective_module.LoadImagesResize(f"{self.params_.path_.root_}/{self.params_.path_.test_defective_}", self.params_.colour_mode_, self.params_.size_)

        print("Converting to DataFrame")
            
        train = DataFrame(train_module.images_)
        test_good = DataFrame(test_good_module.images_)
        test_defective = DataFrame(test_defective_module.images_)

        print("Train Shape: ", train.shape)
        print("Test Good Shape: ", test_good.shape)
        print("Test Defective Shape: ", test_defective.shape)
        print("Data Loaded")

        return train, test_good, test_defective

    def TrainTestSequence(self, *, train : DataFrame, test_good : DataFrame, test_defective : DataFrame, model_type : PyCaretModelUnit.ModelTypeFlag) -> None:
        """
        Train test sequence

        Args:
        train : DataFrame - training data
        test_good : DataFrame - good test data
        test_defective : DataFrame - defective test data
        model_type : PyCaretModelUnit.ModelTypeFlag - model type flag

        Example:
        >>> path = TrainPathObject("train", "test_good", "test_defective")
        >>> train = TrainObject(path, ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
        >>> run = RunPycaret(param=train)
        >>> train, test_good, test_defective = run.LoadData()
        >>> run.TrainTestSequence(train=train, test_good=test_good, test_defective=test_defective, model_type=PyCaretModelUnit.ModelTypeFlag.knn_)
        """
        self.model_.Train(data=train, model_type=model_type)
        # self.model_.Evaluate()
        
        # for plot in PyCaretModelUnit.PlotTypeFlag.tsne_:
        #     self.model_.Plot(plot)

        # self.model_.Save(f"{self.params_.name_}_{PyCaretModelUnit.ModelTypeFlagName[model_type]}")

        # self.model_.Results(test_good, f"{PyCaretModelUnit.ModelTypeFlagName[model_type]}_good")
        # self.model_.Results(test_defective, f"{PyCaretModelUnit.ModelTypeFlagName[model_type]}_defective")

        self.model_.EvaluationMetrics(test_good, test_defective, f"{self.params_.name_}_{PyCaretModelUnit.ModelTypeFlagName[model_type]}")

    def Run(self) -> None:
        """
        Run Pycaret

        Example:
        >>> path = TrainPathObject("train", "test_good", "test_defective")
        >>> train = TrainObject(path, ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
        >>> run = RunPycaret(param=train)
        >>> run.Run()
        """
        train, test_good, test_defective = self.LoadData()

        for model_type in self.model_type_flag_:
            try:
                print(f"Training {model_type}")
                self.TrainTestSequence(train=train, test_good=test_good, test_defective=test_defective, model_type=model_type)
            except Exception as e:
                print(f"Error: {e}")
            continue

class PycaretPredict:
    """
    Pycaret prediction class

    Unimplemented as of now
    """

    def __init__(self, *, param: PredictPathObject):
        ...

def main():
    train_object : TrainObject = TrainObject(TrainPathObject("train", "test_good", "test_defective"), ImageUnit.ColorModeEnum.rgb_, Size(100, 100), "plant")
    
    run = PycaretTrain(param=train_object)
    run.Run()

if __name__ == "__main__":
    main()