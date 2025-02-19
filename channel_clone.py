from discord import Message
from enum import Enum, auto, unique
from classes.discord_lib import MessageObject
from channel_template import ChannelMessageTemplate, CommandObject
from classes.util_lib import Unused
from classes.channel_enum import ChannelEnum
from classes.log_lib import LoggerDiscord

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
    close_ = auto()

# class ChannelMessageDebug(ChannelMessageTemplate):
#     """
#     The ChannelMessageDebug class is used to handle the debug channel messages.

#     Example:
#     >>> channel_message_PREDICT = ChannelMessageDebug()
#     >>> channel_message_PREDICT.RegisterCommand(command_enum=CommandEnum.help_, command_object=CommandObject(name="help", description="Help Command", function=ResHelp))
#     >>> channel_message_PREDICT.RegisterCommand(command_enum=CommandEnum.test_, command_object=CommandObject(name="test", description="Test Command", function=ResTest))
#     >>> channel_message_PREDICT.SetupCommand()
#     >>> channel_message_PREDICT.RunFunc(command_enum=CommandEnum.help_, message=message, message_object=message_object)
#     """

#     def __init__(self) -> None:
#         """
#         Initialize the ChannelMessageDebug class.
#         """
#         super().__init__()

async def ResTest(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system

    This channel can accesss to hidden commands for the system.

    This is a private channel for the system

    TODO REMOVE THIS FUNCTION

    Train ANOMALIV
    """
    await message.create_thread(name="Clone Thread", auto_archive_duration=1440)
    if message.thread is None:
        message_object.CreateEmbed(title="Thread", description="Thread is empty")
    else:
        for a in range(5):
            await message.thread.send(f"Clone {a}")
        message_object.SetMessage("Clone : " + message.content)

CHANNEL_MESSAGE_CLONE : ChannelMessageTemplate = ChannelMessageTemplate()
SHARE_LOGGER : LoggerDiscord = LoggerDiscord()

async def ResHelp(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the help of the system
    """
    Unused(message)
    message_object.CreateEmbed(title="Help", description="Help Command")
    for command_object in CHANNEL_MESSAGE_CLONE.command_object_dict_.values():
        message_object.EmbedAddField(name=command_object.name_, value=command_object.description_)
    
async def ResClone(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system
    """
    if SHARE_LOGGER.thread_ is None:
        message_object.SetMessage("Logger False")
        return

    m_obj = MessageObject()
    m_obj.message_ = " ".join(message.content.split(" ")[1:])
    if len(message.embeds) > 0:
        m_obj.embed_ = message.embeds[0]
    await SHARE_LOGGER.Output(message_object=m_obj)
    message_object.SetMessage("Sent")

async def ResClose(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system
    """
    if SHARE_LOGGER.thread_ is None:
        message_object.SetMessage("Logger False")
        return

    await SHARE_LOGGER.Close()
    message_object.SetMessage("Closed")

def Setup() -> None:
    """
    Setup the ChannelMessageTemplate
    """
    CHANNEL_MESSAGE_CLONE.RegisterCommand(
        command_enum=CommandEnum.help_, 
        command_object=CommandObject(
            name="help", 
            description="Help Command", 
            function=ResHelp))
    CHANNEL_MESSAGE_CLONE.RegisterCommand(
        command_enum=CommandEnum.test_, 
        command_object=CommandObject(
            name="clone", 
            description="Clone Command from This channel to current interest thread", 
            function=ResClone))
    CHANNEL_MESSAGE_CLONE.RegisterCommand(
        command_enum=CommandEnum.prev_, 
        command_object=CommandObject(
            name="test", 
            description="Test Command", 
            function=ResTest))
    CHANNEL_MESSAGE_CLONE.RegisterCommand(
        command_enum=CommandEnum.close_, 
        command_object=CommandObject(
            name="close", 
            description="Close Command", 
            function=ResClose))
    CHANNEL_MESSAGE_CLONE.SetupCommand()