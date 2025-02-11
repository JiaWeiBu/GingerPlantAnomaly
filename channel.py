"""
This file contains the logic for the discord bot,
THis will connect all other files with the bot,
register the channels and send the message to the bot
and manage the callback functions for the bot
"""

from typing import Any
from os import getenv
from enum import Enum, auto, unique
from dotenv import load_dotenv
from random import randint
from discord import Message
from classes.discord_lib import MessageObject
from classes.message_lib import MessageUnit, INIT_PHRASE, WebhookSend, ChannelObject
import channel_debug
import channel_predict
import channel_log

load_dotenv()
MESSAGE_UNIT = MessageUnit(keyword="~")
channel_debug.Setup()
channel_predict.Setup()
channel_log.Setup()

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

def RegisterChannelConfig() -> None:
    """
    Function to register the channels
    """
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.log_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_LOG", webhook_url="", func=channel_log.CHANNEL_MESSAGE_LOG.ResMessage, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.predict_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_PREDICT", webhook_url="", func=channel_predict.CHANNEL_MESSAGE_PREDICT.ResMessage, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.debug_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_DEBUG", webhook_url="", func=channel_debug.CHANNEL_MESSAGE_DEBUG.ResMessage, password=0))

    channel_debug.CHANNEL_MESSAGE_DEBUG.ImportChannelObject(channel_object=MESSAGE_UNIT.channel_object_dict_[ChannelEnum.debug_])
    channel_predict.CHANNEL_MESSAGE_PREDICT.ImportChannelObject(channel_object=MESSAGE_UNIT.channel_object_dict_[ChannelEnum.predict_])
    channel_log.CHANNEL_MESSAGE_LOG.ImportChannelObject(channel_object=MESSAGE_UNIT.channel_object_dict_[ChannelEnum.log_])

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
        MESSAGE_UNIT.SetChannelPass(channel=channel, pass_=randint(10000000, 99999999))

        # Send the passcode to the channel
        await WebhookSend(webhook_url=MESSAGE_UNIT.channel_object_dict_[channel].webhook_url_, content=f"{MESSAGE_UNIT.keyword_}{INIT_PHRASE} {MESSAGE_UNIT.channel_object_dict_[channel].pass_}")
    
    print(f"Init Configurations are done")

async def LogSend(message: str) -> None:
    """
    Function to send the log message

    Args:
    - message : str - The message to be sent
    """
    await WebhookSend(webhook_url=MESSAGE_UNIT.channel_object_dict_[ChannelEnum.log_].webhook_url_, content=message)