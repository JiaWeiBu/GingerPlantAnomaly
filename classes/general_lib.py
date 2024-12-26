from classes.util_lib import Size
from classes.dataset_lib import ImageUnit

class PredictPathObject:
    """
    Path object for prediction

    Attributes:
    model_ : str - path to model
    test_good_ : str - path to good test data
    test_defective_ : str - path to defective test data

    Example:
    >>> path = PredictPathObject("model.pt", "test_good", "test_defective")
    >>> path.test_good_
    "test_good"
    >>> path.test_defective_
    "test_defective"
    """
    root_ : str
    model_ : str
    test_good_ : str
    test_defective_ : str

class TrainPathObject:
    """
    Path object for training

    Attributes:
    train_ : str - path to training data
    test_good_ : str - path to good test data
    test_defective_ : str - path to defective test data

    Example:
    >>> path = TrainPathObject("train", "test_good", "test_defective")
    >>> path.train_
    "train"
    >>> path.test_good_
    "test_good"
    >>> path.test_defective_
    "test_defective"
    """
    root_ : str
    train_ : str
    test_good_ : str
    test_defective_ : str
    model_save_ : str

class TrainObject:
    """
    Train object for training

    Attributes:
    path_ : TrainPathObject - path object for training
    colour_mode_ : ImageUnit.ColorModeEnum - colour mode for training
    size_ : Size[int] - size of image for training
    name_ : str - name of the training project

    Example:
    >>> path = TrainPathObject("train", "test_good", "test_defective")
    >>> train = TrainObject(path, ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
    >>> train.path_
    "train"
    >>> train.colour_mode_
    ImageUnit.ColorModeEnum.rgb_
    >>> train.size_
    Size(100, 100)
    """
    path_ : TrainPathObject
    colour_mode_ : ImageUnit.ColorModeEnum
    size_ : Size[int]
    name_ : str 