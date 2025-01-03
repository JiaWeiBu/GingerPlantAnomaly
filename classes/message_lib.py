from typing import Callable, Any
from enum import Enum, unique, auto
from classes.discord_lib import MessageObject
from discord import Message, Webhook
from aiohttp import ClientSession

INIT_PHRASE : str = "ginie"

# Webhook 
async def WebhookSend(webhook_url : str, *, content: str) -> None:
    """
    Sends a message to the webhook URL.

    Args:
    - webhook_url (str): The URL of the webhook.
    - content (str): The content of the message.

    Example:
    >>> await WebhookSend("https://discord.com/api/webhooks/123456789", content="Hello World")
    """
    async with ClientSession() as session:
        await Webhook.from_url(webhook_url, session=session).send(content=content)

# Discord Message Bot
class MessageUnit:
    """
    Class for the message unit

    Steps:
    1. Set the pass for the channels
    2. Send the password and it will automatically set the channel ID
    3. Initialize the channels
    4. Run the functions for the channels
    """
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

    class ChannelObject:
        """
        Class for the channel object

        Attributes:
        - id_ (int): The channel ID
        - webhook_env_ (str): The webhook environment variable
        - webhook_url_ (str): The webhook URL
        - func_ (Callable): The function to run for the channel
        - pass_ (int): The password for the channel
        """
        def __init__(self, ids : int, webhook_env : str, webhook_url : str, func : Callable, password : int) -> None:
            self.id_ : int = ids
            self.webhook_env_ : str = webhook_env
            self.webhook_url_ : str = webhook_url
            self.func_ : Callable = func
            self.pass_ : int = password

    def __init__(self) -> None:
        self.channel_id_dict_inv_ : dict[int, self.ChannelEnum] = {}
        self.channel_object_dict_ : dict[self.ChannelEnum, self.ChannelObject] = {
            self.ChannelEnum.log_ : self.ChannelObject(0, "CHANNEL_WEBHOOK_LOG", "", self.ResLog, 0),
            self.ChannelEnum.predict_ : self.ChannelObject(0, "CHANNEL_WEBHOOK_PREDICT", "", self.ResPredict, 0),
            self.ChannelEnum.debug_ : self.ChannelObject(0, "CHANNEL_WEBHOOK_DEBUG", "", self.ResDebug, 0),
        }
        self.init_ : bool = False
        self.num_channels_init_ : int = len(self.channel_object_dict_)

    def SetChannelID(self, *, channel : ChannelEnum, channel_id : int) -> None:
        """
        Sets the channel ID for a given channel.

        Args:
        - channel (ChannelEnum): The channel to set the ID for.
        - channel_id (int): The ID to set for the channel.

        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.SetChannelID(channel=MessageUnit.ChannelEnum.log_, channel_id=123456789)
        """
        self.channel_object_dict_[channel].id_ = channel_id

    def SetChannelPass(self, *, channel : ChannelEnum, pass_ : int) -> None:
        """
        Sets the pass for the channel.

        Args:
        - channel (ChannelEnum): The channel to set the pass for.
        - pass_ (int): The pass to set for the channel.

        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.SetChannelPass(channel=MessageUnit.ChannelEnum.log_, pass_=123456789)
        """
        self.channel_object_dict_[channel].pass_ = pass_

    def SetChannelWebhookUrl(self, *, channel : ChannelEnum, webhook_url : str) -> None:
        """
        Sets the webhook URL for the channel.

        Args:
        - channel (ChannelEnum): The channel to set the webhook URL for.
        - webhook_url (str): The webhook URL to set for the channel.

        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.SetChannelWebhookUrl(channel=MessageUnit.ChannelEnum.log_, webhook_url="https://discord.com/api/webhooks/123456789")
        """
        self.channel_object_dict_[channel].webhook_url_ = webhook_url

    def ChannelDictInit(self) -> None:
        """
        Initializes the channel ID sets.

        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.SetChannelID(channel=MessageUnit.ChannelEnum.log_, channel_id=123456789)
        >>> message_unit.ChannelSetInit()
        """
        self.channel_id_dict_inv_ = {v.id_: k for k, v in self.channel_object_dict_.items()}

        assert 0 not in self.channel_id_dict_inv_, "Channel IDs not set"

        self.init_ = True
    
    def RunFunc(self, *, func : Callable[[Message], MessageObject], message : Message) -> MessageObject:
        """
        Runs the function for the given message.

        Args:
        - func (Callable[[Message], MessageObject]): The function to run.
        - message (Message): The message to run the function on.

        Returns:
        - MessageObject: The message object returned by the function.

        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.RunFunc(func=message_unit.ResLog, message=discord.Message)
        """
        return func(message)

    def GetResponse(self, message : Message) -> MessageObject:
        """
        Gets the response for the given message.
        Checks if the message is in the correct channel and runs the function for the channel.

        Args:
        - message (Message): The message to get the response for.

        Returns:
        - MessageObject: The message object returned by the function.
        
        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.SetChannelID(channel=MessageUnit.ChannelEnum.log_, channel_id=123456789)
        >>> message_unit.ChannelSetInit()
        >>> message_unit.GetResponse(discord.Message)
        """
        message_object = MessageObject()
        if not self.init_:
            content : Any = message.content.split(" ")
            word = content[0].lower()
            content = " ".join(content[1:])
            if word == INIT_PHRASE:
                for channel, channel_object in self.channel_object_dict_.items():
                    try:
                        if int(content) == channel_object.pass_:
                            self.SetChannelID(channel=channel, channel_id=message.channel.id)
                            message_object.SetMessage("Channel ID set")

                            self.num_channels_init_ -= 1
                            if self.num_channels_init_ == 0:
                                self.ChannelDictInit()
                                message_object.SetMessage("Channel ID set\nAll channels initialized")
                    except ValueError:
                        message_object.SetMessage("Invalid pass")
                        break
            else:
                message_object.SetMessage(f"System not initialized yet")
        else: 
            if message.channel.id in self.channel_id_dict_inv_:
                message_object = self.RunFunc(func=self.channel_object_dict_[self.channel_id_dict_inv_[message.channel.id]].func_, message=message)

        return message_object

    def ResLog(self, message : Message) -> MessageObject:
        """
        """
        message_object = MessageObject()
        message_object.SetMessage("Log : " + message.content)

        return message_object

    def ResPredict(self, message : Message) -> MessageObject:
        """
        """
        message_object = MessageObject()
        message_object.CreateEmbed(title="Test", description="Test Description")

        return message_object

    def ResDebug(self, message : Message) -> MessageObject:
        """
        """
        message_object = MessageObject()
        message_object.SetFile("./datasets/re_plant/train/60/00001.jpg", filename="test.jpg", description="Test Description")
        message_object.SetMessage("Debug : " + message.content)
        message_object.CreateEmbed(title="Test Image", description="Test Image Description")
        message_object.EmbedSetImage(url="attachment://test.jpg")

        return message_object