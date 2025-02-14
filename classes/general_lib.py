from typing import Dict, Type, TypeVar, Callable
from asyncio import run
from classes.util_lib import Size
from classes.dataset_lib import ImageUnit

T = TypeVar("T", bound="Base")

def Singleton(cls: Type[T]) -> Type[T]:
    """
    Singleton decorator ensuring each class has its own unique instance.

    Args:
        cls (Type[T]): The class to be made singleton.

    Returns:
        Type[T]: The singleton class.
    """
    instances: Dict[Type[T], T] = {}

    class SingletonWrapper(cls):  # Inherit from cls to keep methods
        def __new__(subcls, *args, **kwargs):  
            if subcls not in instances:
                instance = super().__new__(subcls)  # Create new instance
                instances[subcls] = instance
            return instances[subcls]

        def __init__(self, *args, **kwargs):
            """ Ensure __init__ is only called once per class instance """
            if not hasattr(self, "_initialized"):
                super().__init__(*args, **kwargs)
                self._initialized = True  # Mark as initialized

    return SingletonWrapper  # Return modified class

def AsyncThread(func : Callable, *args, **kwargs) -> None:
    """
    Run the async function in a new thread
    """
    run(func(*args, **kwargs))

class PredictPathObject:
    """
    Path object for prediction

    Attributes:
    root_ : str - root path for prediction
    model_ : str - path to model
    test_good_ : str - path to good test data
    test_defective_ : str - path to defective test data

    TODO : Missing from bottom of the file
    
    Example:
    >>> path = PredictPathObject("model.pt", "test_good", "test_defective")
    >>> path.test_good_
    "test_good"
    >>> path.test_defective_
    "test_defective"
    """
    def __init__(self, root : str, model : str, test_good : str, test_defective : str) -> None:
        self.root_ : str = root
        self.model_ : str = model
        self.test_good_ : str = test_good
        self.test_defective_ : str = test_defective
     
class TrainPathObject:
    """
    Path object for training

    Attributes:
    root_ : str - root path for training
    train_ : list[str] - path to training data
    test_good_ : list[str] - path to good test data
    test_defective_ : list[str] - path to defective test data
    model_save_ : str - path to save model

    Example:
    >>> path = TrainPathObject("root", "train", "test_good", "test_defective", "model_save")
    >>> path.train_
    "train"
    >>> path.test_good_
    "test_good"
    >>> path.test_defective_
    "test_defective"
    """

    def __init__(self, root : str, train : list[str], test_good : list[str], test_defective : list[str], model_save : str) -> None:
        self.root_ : str = root
        self.train_ : list[str] = train
        self.test_good_ : list[str] = test_good
        self.test_defective_ : list[str] = test_defective
        self.model_save_ : str = model_save

class TrainObject:
    """
    Train object for training

    Attributes:
    path_ : TrainPathObject - path object for training
    colour_mode_ : ImageUnit.ColorModeEnum - colour mode for training
    size_ : Size[int] - size of image for training
    name_ : str - name of the training project

    Example:
    >>> train = TrainObject(TrainPathObject("root", "train", "test_good", "test_defective", "model_save"), ImageUnit.ColorModeEnum.rgb_, Size(100, 100), "train")
    >>> train.path_
    "train"
    >>> train.colour_mode_
    ImageUnit.ColorModeEnum.rgb_
    >>> train.size_
    Size(100, 100)
    """
    def __init__(self, path : TrainPathObject, colour_mode : ImageUnit.ColorModeEnum, size : Size[int], name : str) -> None:
        self.path_ : TrainPathObject = path
        self.colour_mode_ : ImageUnit.ColorModeEnum = colour_mode
        self.size_ : Size[int] = size
        self.name_ : str = name