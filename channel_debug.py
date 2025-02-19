from discord import Message
from enum import Enum, auto, unique

from anomalib_train import RunModelAsync
from channel_template import ChannelMessageTemplate, CommandObject
from classes.discord_lib import MessageObject
from classes.util_lib import Unused
from classes.channel_enum import ChannelEnum, CHANNEL_KEYWORD
from classes.log_lib import LoggerDiscord
from classes.anomalib_lib import AnomalyModelUnit

@unique
class CommandEnum(Enum):
    """
    Enum class for the command IDs

    Attributes:
    help_: Help command ID
    test_: Test command ID

    Example:
    >>> command_enum = CommandEnum.help_
    """
    help_ = auto()
    test_ = auto()
    prev_ = auto()
    train_ = auto()

# class ChannelMessageDebug(ChannelMessageTemplate):
#     """
#     The ChannelMessageDebug class is used to handle the debug channel messages.

#     Example:
#     >>> channel_message_debug = ChannelMessageDebug()
#     >>> channel_message_debug.RegisterCommand(command_enum=CommandEnum.help_, command_object=CommandObject(name="help", description="Help Command", function=ResHelp))
#     >>> channel_message_debug.RegisterCommand(command_enum=CommandEnum.test_, command_object=CommandObject(name="test", description="Test Command", function=ResTest))
#     >>> channel_message_debug.SetupCommand()
#     >>> channel_message_debug.RunFunc(command_enum=CommandEnum.help_, message=message, message_object=message_object)
#     """

#     def __init__(self) -> None:
#         """
#         Initialize the ChannelMessageDebug class.
#         """
#         super().__init__()

async def ResDebug(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the debug of the system

    This channel can accesss to hidden commands for the system.

    This is a private channel for the system

    TODO REMOVE THIS FUNCTION

    Train ANOMALIV
    """
    message_object.SetFile("./datasets/re_plant/train/60/00001.jpg", filename="test.jpg", description="Test Description")
    message_object.SetMessage("Debug : " + message.content)
    message_object.CreateEmbed(title="Test Image", description="Test Image Description")
    message_object.EmbedSetImage(url="attachment://test.jpg")

CHANNEL_MESSAGE_DEBUG : ChannelMessageTemplate = ChannelMessageTemplate()
SHARE_LOGGER : LoggerDiscord = LoggerDiscord()

async def ResHelp(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the help of the system
    """
    Unused(message)
    message_object.CreateEmbed(title="Help", description="Help Command")
    for command_object in CHANNEL_MESSAGE_DEBUG.command_object_dict_.values():
        message_object.EmbedAddField(name=command_object.name_, value=command_object.description_)
    
async def ResTest(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system
    """
    message_object.SetMessage(f"Thread : {SHARE_LOGGER.thread_}")

async def ResTrain(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the train of the system
    """
    message_object.SetMessage("Train : " + message.content)
    assert CHANNEL_MESSAGE_DEBUG.channel_object_dict_ is not None, "channel_object_dict is None"
    assert ChannelEnum.log_ in CHANNEL_MESSAGE_DEBUG.channel_object_dict_, "log_ is not in channel_object_dict"
    content : str = " ".join(message.content.split(" ")[1:])

    await SHARE_LOGGER.Setup(webhook_link=CHANNEL_MESSAGE_DEBUG.channel_object_dict_[ChannelEnum.log_].webhook_url_, name=f"{CHANNEL_KEYWORD}train {content}")

    message_object.SetMessage(f"Train : {content} started")

def Setup() -> None:
    """
    Setup the ChannelMessageTemplate
    """
    CHANNEL_MESSAGE_DEBUG.RegisterCommand(
        command_enum=CommandEnum.help_, 
        command_object=CommandObject(
            name="help", 
            description="Help Command", 
            function=ResHelp))
    CHANNEL_MESSAGE_DEBUG.RegisterCommand(
        command_enum=CommandEnum.test_, 
        command_object=CommandObject(
            name="test", 
            description="Test Command", 
            function=ResTest))
    CHANNEL_MESSAGE_DEBUG.RegisterCommand(
        command_enum=CommandEnum.prev_, 
        command_object=CommandObject(
            name="prev", 
            description="Prev Command", 
            function=ResDebug))
    CHANNEL_MESSAGE_DEBUG.RegisterCommand(
        command_enum=CommandEnum.train_, 
        command_object=CommandObject(
            name="train", 
            description="Train Command", 
            function=ResTrain))
    CHANNEL_MESSAGE_DEBUG.SetupCommand()