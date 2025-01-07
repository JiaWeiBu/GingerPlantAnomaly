"""
This file contains the logic for the discord bot,
THis will connect all other files with the bot,
register the channels and send the message to the bot
and manage the callback functions for the bot
"""

from os import getenv
from enum import Enum, auto, unique
from dotenv import load_dotenv
from random import randint
from discord import Message
from classes.discord_lib import MessageObject
from classes.message_lib import MessageUnit, INIT_PHRASE, WebhookSend

load_dotenv()
MESSAGE_UNIT = MessageUnit(keyword="~")

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

# Temporary Placeholder
async def ResLog(message : Message, message_object : MessageObject) -> None:
        """
        This is used as a logging for the system

        This is a private channel for the system

        TODO REMOVE THIS FUNCTION
        """
        message_object.SetMessage("Log : " + message.content)

async def ResPredict(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the prediction of the system
    It will be samme like chatgpt

    TODO REMOVE THIS FUNCTION
    """
    await message.create_thread(name="Prediction Thread", auto_archive_duration=1440)
    if message.thread is None:
        message_object.CreateEmbed(title="Thread", description="Thread is empty")
    else:
        for a in range(5):
            await message.thread.send(f"Prediction {a}")
        message_object.SetMessage("Predict : " + message.content)

async def ResDebug(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the debug of the system

    This channel can accesss to hidden commands for the system.

    This is a private channel for the system

    TODO REMOVE THIS FUNCTION
    """
    message_object.SetFile("./datasets/re_plant/train/60/00001.jpg", filename="test.jpg", description="Test Description")
    message_object.SetMessage("Debug : " + message.content)
    message_object.CreateEmbed(title="Test Image", description="Test Image Description")
    message_object.EmbedSetImage(url="attachment://test.jpg")

def RegisterChannelConfig() -> None:
    """
    Function to register the channels
    """
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.log_, channel_object=MESSAGE_UNIT.ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_LOG", webhook_url="", func=ResLog, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.predict_, channel_object=MESSAGE_UNIT.ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_PREDICT", webhook_url="", func=ResPredict, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.debug_, channel_object=MESSAGE_UNIT.ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_DEBUG", webhook_url="", func=ResDebug, password=0))


async def SendMessage(message: Message) -> None:
    response : MessageObject = await MESSAGE_UNIT.GetResponse(message)

    if not response.EmptyMessage():
        await message.channel.send(response.message_, embed=response.embed_, file=response.file_) # type: ignore

async def RegisterChannel() -> None:
    """
    Function to register the channels
    """
    print(f"Setting up the channels")
    for channel in ChannelEnum:
        # Load the webhook url from the environment
        MESSAGE_UNIT.SetChannelWebhookUrl(channel=channel, webhook_url=str(getenv(MESSAGE_UNIT.channel_object_dict_[channel].webhook_env_)))
        
        # Set the passcode for the channel
        MESSAGE_UNIT.SetChannelPass(channel=channel, pass_=randint(100000, 999999))

        # Send the passcode to the channel
        await WebhookSend(webhook_url=MESSAGE_UNIT.channel_object_dict_[channel].webhook_url_, content=f"{MESSAGE_UNIT.keyword_}{INIT_PHRASE} {MESSAGE_UNIT.channel_object_dict_[channel].pass_}")
    
    print(f"Init Configurations are done")