from enum import Enum, auto, unique

CHANNEL_KEYWORD : str = "~"

@unique
class ChannelEnum(Enum):
    """
    Enum class for the channel IDs

    Attributes:
    - log_: Log channel ID
    - predict_: Prediction channel ID, user sends images and message to be answered
    - debug_: Debug channel ID for train or debug purposes
    """
    log_ = auto()
    predict_ = auto()
    debug_ = auto()
    clone_ = auto()