from typing import Dict, Type, TypeVar, Callable
from asyncio import run_coroutine_threadsafe, AbstractEventLoop, set_event_loop
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

class ImageInfoObject:
    """
    Image information object

    Attributes:
    size_ : Size[int] - size of image
    colour_mode_ : ImageUnit.ColorModeEnum - colour mode of image
    name_ : str - name of the image

    Example:
    >>> img_info = ImageInfoObject(Size(100, 100), ImageUnit.ColorModeEnum.rgb_, "image_name")
    >>> img_info.size_
    Size(100, 100)
    >>> img_info.colour_mode_
    ImageUnit.ColorModeEnum.rgb_
    >>> img_info.name_
    "image_name"
    """
    def __init__(self, size : Size[int], colour_mode : ImageUnit.ColorModeEnum, name : str) -> None:
        self.size_ : Size[int] = size
        self.colour_mode_ : ImageUnit.ColorModeEnum = colour_mode
        self.name_ : str = name
     
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
    image_info_ : ImageInfoObject - image information object for training

    Example:
    >>> train = TrainObject(TrainPathObject("root", "train", "test_good", "test_defective", "model_save"), ImageInfoObject(Size(100, 100), ImageUnit.ColorModeEnum.rgb_, "image_name"))
    >>> train.path_
    "train"
    >>> train.image_info_.colour_mode_
    ImageUnit.ColorModeEnum.rgb_
    >>> train.image_info_.size_
    Size(100, 100)
    >>> train.image_info_.name_
    "image_name"
    """
    def __init__(self, path : TrainPathObject, image_info : ImageInfoObject) -> None:
        self.path_ : TrainPathObject = path
        self.image_info_ : ImageInfoObject = image_info

class TestPathObject:
    """
    Path object for testing

    Attributes:
    root_ : str - root path for testing
    test_good_ : list[str] - path to good test data
    test_defective_ : list[str] - path to defective test data

    Example:
    >>> path = TestPathObject("root", "test_good", "test_defective")
    >>> path.test_good_
    "test_good"
    >>> path.test_defective_
    "test_defective"
    """
    def __init__(self, root : str, test_good : list[str], test_defective : list[str], test_mask : list[str]) -> None:
        self.root_ : str = root
        self.test_good_ : list[str] = test_good
        self.test_defective_ : list[str] = test_defective
        self.test_mask_ : list[str] = test_mask

class TestObject:
    """
    Test object for testing

    Attributes:
    path_ : TestPathObject - path object for testing
    image_info_ : ImageInfoObject - image information object for testing

    Example:
    >>> test = TestObject(TestPathObject("root", "test_good", "test_defective", "test_mask"), ImageInfoObject(Size(100, 100), ImageUnit.ColorModeEnum.rgb_, "test"))
    >>> test.path_
    "test"
    >>> test.image_info_.colour_mode_
    ImageUnit.ColorModeEnum.rgb_
    >>> test.image_info_.size_
    Size(100, 100)
    >>> test.image_info_.name_
    "test"
    """
    def __init__(self, path : TestPathObject, image_info: ImageInfoObject) -> None:
        self.path_ : TestPathObject = path
        self.image_info_ : ImageInfoObject = image_info