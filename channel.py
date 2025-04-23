"""
This file contains the logic for the discord bot,
THis will connect all other files with the bot,
register the channels and send the message to the bot
and manage the callback functions for the bot
"""

from os import getenv
from dotenv import load_dotenv
from random import randint
from discord import Message
from classes.discord_lib import MessageObject
from classes.message_lib import MessageUnit, INIT_PHRASE, WebhookSend, ChannelObject
from classes.channel_enum import ChannelEnum, CHANNEL_KEYWORD
import channel_debug
import channel_predict
import channel_log
import channel_clone

load_dotenv()
MESSAGE_UNIT = MessageUnit(keyword=CHANNEL_KEYWORD)
channel_debug.Setup()
channel_predict.Setup()
channel_log.Setup()
channel_clone.Setup()

def RegisterChannelConfig() -> None:
    """
    Function to register the channels
    """
    # Register the channels
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.log_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_LOG", webhook_url="", func=channel_log.CHANNEL_MESSAGE_LOG.ResMessage, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.predict_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_PREDICT", webhook_url="", func=channel_predict.CHANNEL_MESSAGE_PREDICT.ResMessage, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.debug_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_DEBUG", webhook_url="", func=channel_debug.CHANNEL_MESSAGE_DEBUG.ResMessage, password=0))
    MESSAGE_UNIT.RegisterChannelObject(channel=ChannelEnum.clone_, channel_object=ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_CLONE", webhook_url="", func=channel_clone.CHANNEL_MESSAGE_CLONE.ResMessage, password=0))

    # Reverse by returning the channel object to their respective channels
    channel_debug.CHANNEL_MESSAGE_DEBUG.ImportChannelObjectDict(channel_object_dict=MESSAGE_UNIT.channel_object_dict_)
    channel_predict.CHANNEL_MESSAGE_PREDICT.ImportChannelObjectDict(channel_object_dict=MESSAGE_UNIT.channel_object_dict_)
    channel_log.CHANNEL_MESSAGE_LOG.ImportChannelObjectDict(channel_object_dict=MESSAGE_UNIT.channel_object_dict_)
    channel_clone.CHANNEL_MESSAGE_CLONE.ImportChannelObjectDict(channel_object_dict=MESSAGE_UNIT.channel_object_dict_)

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
        
        message_object = MessageObject()
        message_object.SetMessage(f"{MESSAGE_UNIT.keyword_}{INIT_PHRASE} {MESSAGE_UNIT.channel_object_dict_[channel].pass_}")
        # Send the passcode to the channel
        await WebhookSend(webhook_url=MESSAGE_UNIT.channel_object_dict_[channel].webhook_url_, message_object=message_object)
    
    print(f"Init Configurations are done")