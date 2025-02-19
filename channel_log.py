from discord import Message
from enum import Enum, auto, unique
from dotenv import load_dotenv
from requests import Response, get
from classes.discord_lib import MessageObject
from channel_template import ChannelMessageTemplate, CommandObject
from classes.util_lib import Unused
from classes.log_lib import LoggerDiscord
from classes.channel_enum import ChannelEnum, CHANNEL_KEYWORD

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
#     >>> channel_message_LOG = ChannelMessageDebug()
#     >>> channel_message_LOG.RegisterCommand(command_enum=CommandEnum.help_, command_object=CommandObject(name="help", description="Help Command", function=ResHelp))
#     >>> channel_message_LOG.RegisterCommand(command_enum=CommandEnum.test_, command_object=CommandObject(name="test", description="Test Command", function=ResTest))
#     >>> channel_message_LOG.SetupCommand()
#     >>> channel_message_LOG.RunFunc(command_enum=CommandEnum.help_, message=message, message_object=message_object)
#     """

#     def __init__(self) -> None:
#         """
#         Initialize the ChannelMessageDebug class.
#         """
#         super().__init__()

async def ResLog(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the debug of the system

    This channel can accesss to hidden commands for the system.

    This is a private channel for the system

    TODO REMOVE THIS FUNCTION

    Train ANOMALIV
    """
    await message.create_thread(name="Log Thread", auto_archive_duration=1440)
    if message.thread is None:
        message_object.CreateEmbed(title="Thread", description="Thread is empty")
    else:
        for a in range(5):
            await message.thread.send(f"Log {a}")
        message_object.SetMessage("Log : " + message.content)

CHANNEL_MESSAGE_LOG : ChannelMessageTemplate = ChannelMessageTemplate()
SHARE_LOGGER : LoggerDiscord = LoggerDiscord()

async def ResHelp(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the help of the system
    """
    Unused(message)
    message_object.CreateEmbed(title="Help", description="Help Command")
    for command_object in CHANNEL_MESSAGE_LOG.command_object_dict_.values():
        message_object.EmbedAddField(name=command_object.name_, value=command_object.description_)
    
async def ResTest(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system
    """
    message_object.SetMessage("Running Test: " + message.content)

async def ResTrain(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the train of the system
    """
    # await message.create_thread(name=f"{message.content} Thread", auto_archive_duration=1440)
    # if message.thread is None:
    #     message_object.CreateEmbed(title="Thread", description="Thread is empty")
    # else:
    #     for a in range(5):
    #         await message.thread.send(f"Train {a}")
    await SHARE_LOGGER.Open(message=message, name=f'{" ".join(message.content.split(" ")[1:])} Thread', duration=1440)

    # send to flask to train the model
    get(f"http://127.0.0.1:5000/train")

    message_object.SetMessage(f"Succesfully started training: {' '.join(message.content.split(' ')[1:])}")

def Setup() -> None:
    """
    Setup the ChannelMessageTemplate
    """
    CHANNEL_MESSAGE_LOG.RegisterCommand(
        command_enum=CommandEnum.help_, 
        command_object=CommandObject(
            name="help", 
            description="Help Command", 
            function=ResHelp))
    CHANNEL_MESSAGE_LOG.RegisterCommand(
        command_enum=CommandEnum.test_, 
        command_object=CommandObject(
            name="test", 
            description="Test Command", 
            function=ResTest))
    CHANNEL_MESSAGE_LOG.RegisterCommand(
        command_enum=CommandEnum.prev_, 
        command_object=CommandObject(
            name="prev",  
            description="Prev Command", 
            function=ResLog))
    CHANNEL_MESSAGE_LOG.RegisterCommand(
        command_enum=CommandEnum.train_, 
        command_object=CommandObject(
            name="train", 
            description="Train Log Output (INTERNAL)", 
            function=ResTrain))
    CHANNEL_MESSAGE_LOG.SetupCommand()