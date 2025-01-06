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

    How it works:
    1. Set the pass for the channels
    2. Send the password and it will automatically set the channel ID
    3. Initialize the channels
    4. Run the functions for the channels

    What to do:
    1. Register the channels and their method

    Attributes:
    - ChannelEnum (Enum): Enum class for the channel IDs
    - ChannelObject (Class): Class for the channel object
    - channel_id_dict_inv_ (dict[int, ChannelEnum]): The dictionary for the channel ID.
    - channel_object_dict_ (dict[ChannelEnum, ChannelObject]): The dictionary for the channel object.
    - init_ (bool): The flag to check if the system is initialized.
    - num_channels_init_ (int): The number of channels to initialize.
    - keyword_ (str): The keyword to check for the message.

    Classes:
    - ChannelEnum: Enum class for the channel IDs
    - ChannelObject: Class for the channel object

    Methods:
    - SetChannelID: Sets the channel ID for a given channel.
    - SetChannelPass: Sets the pass for the channel.
    - SetChannelWebhookUrl: Sets the webhook URL for the channel.
    - ChannelDictInit: Initializes the channel ID sets.
    - RunFunc: Runs the function for the given message.
    - GetResponse: Gets the response for the given message.
    - InitRoutine: Initializes the system by setting the channel ID based on the password created using your own OTP.
    - ResLog: This is used as a logging for the system using the log channel from Discord.
    - ResPredict: This is used for the prediction of the system using the prediction channel from Discord.
    - ResDebug: This is used for the debug of the system using the debug channel from Discord.

    Example:
    >>> message_unit = MessageUnit()
    >>> message_unit.SetChannelPass("password")
    >>> message_unit.InitRoutine()
    >>> response = message_unit.GetResponse("message")
    >>> print(response)
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
        def __init__(self, *, ids : int, webhook_env : str, webhook_url : str, func : Callable, password : int) -> None:
            """
            Initializes the channel object.

            Args:
            - ids (int): The channel ID
            - webhook_env (str): The webhook environment variable
            - webhook_url (str): The webhook URL
            - func (Callable): The function to run for the channel
            - password (int): The password for the channel

            Attributes:
            - id_ (int): The channel ID
            - webhook_env_ (str): The webhook environment variable
            - webhook_url_ (str): The webhook URL
            - func_ (Callable): The function to run for the channel
            - pass_ (int): The password for the channel

            Example:
            >>> channel_object = ChannelObject(ids=123456789, webhook_env="CHANNEL_WEBHOOK_LOG", webhook_url="", func=ResLog, password=123456789)
            """
            self.id_ : int = ids
            self.webhook_env_ : str = webhook_env
            self.webhook_url_ : str = webhook_url
            self.func_ : Callable = func
            self.pass_ : int = password

    def __init__(self, keyword) -> None:
        """
        Initializes the message unit.

        Args:
        - keyword (str): The keyword to check for the message.

        Attributes:
        - channel_id_dict_inv_ (dict[int, ChannelEnum]): The dictionary for the channel ID.
        - channel_object_dict_ (dict[ChannelEnum, ChannelObject]): The dictionary for the channel object.
        - init_ (bool): The flag to check if the system is initialized.
        - num_channels_init_ (int): The number of channels to initialize.
        - keyword_ (str): The keyword to check for the message.
        """
        self.channel_id_dict_inv_ : dict[int, self.ChannelEnum] = {}
        self.channel_object_dict_ : dict[self.ChannelEnum, self.ChannelObject] = {
            self.ChannelEnum.log_ : self.ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_LOG", webhook_url="", func=self.ResLog, password=0),
            self.ChannelEnum.predict_ : self.ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_PREDICT", webhook_url="", func=self.ResPredict, password=0),
            self.ChannelEnum.debug_ : self.ChannelObject(ids=0, webhook_env="CHANNEL_WEBHOOK_DEBUG", webhook_url="", func=self.ResDebug, password=0),
        }
        self.init_ : bool = False
        self.num_channels_init_ : int = len(self.channel_object_dict_)
        self.keyword_ : str = keyword

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
    
    async def RunFunc(self, *, func : Callable[[Message, MessageObject], None], message : Message, message_object : MessageObject) -> None:
        """
        Runs the function for the given message.

        Args:
        - func (Callable): The function to run.
        - message (Message): The message to run the function for.
        - message_object (MessageObject): The message object to store the response.

        Example:
        >>> message_unit = MessageUnit()
        >>> message_unit.RunFunc(func=message_unit.ResLog, message=discord.Message)
        """
        await func(message, message_object) # type: ignore

    async def GetResponse(self, message : Message) -> MessageObject:
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

        # Check if the system is initialized
        if not self.init_:
            self.InitRoutine(message=message, message_object=message_object)
            return message_object
        
        # Validate the channel
        if message.channel.id in self.channel_id_dict_inv_:
            await self.RunFunc(func=self.channel_object_dict_[self.channel_id_dict_inv_[message.channel.id]].func_, message=message, message_object=message_object)
            return message_object
       
        # Default message
        message_object.SetMessage(f"Hello how are you? {message.content}")
        return message_object

    def InitRoutine(self, message : Message, message_object : MessageObject):
        """
        Initializes the system by
        !. Setting the channel ID based on the password created using your own OTP
        2. The system will read the message and set the channel ID based on the password
        3. Once all the channels are initialized, the system will run the functions for the channels

        Args:
        - message (Message): The message to initialize the system.
        - message_object (MessageObject): The message object to store the response.

        Example:
        >>> message_unit = MessageUnit()
        >>> for channel in MESSAGE_UNIT.ChannelEnum:
        >>>     MESSAGE_UNIT.SetChannelWebhookUrl(channel=channel, webhook_url=str(getenv(MESSAGE_UNIT.channel_object_dict_[channel].webhook_env_)))
        >>>     MESSAGE_UNIT.SetChannelPass(channel=channel, pass_=randint(100000, 999999))
        >>>     await WebhookSend(webhook_url=MESSAGE_UNIT.channel_object_dict_[channel].webhook_url_, content=f"{MESSAGE_UNIT.keyword_}{INIT_PHRASE} {MESSAGE_UNIT.channel_object_dict_[channel].pass_}")
        >>> message_unit.InitRoutine(discord.Message)
        """
        content : Any = message.content[len(self.keyword_):].split(" ")
        if content[0] == INIT_PHRASE:
            for channel, channel_object in self.channel_object_dict_.items():
                try:
                    if int(content[1]) == channel_object.pass_:
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

    async def ResLog(self, message : Message, message_object : MessageObject) -> None:
        """
        This is used as a logging for the system

        This is a private channel for the system

        TODO REMOVE THIS FUNCTION
        """
        message_object.SetMessage("Log : " + message.content)

    async def ResPredict(self, message : Message, message_object : MessageObject) -> None:
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

    async def ResDebug(self, message : Message, message_object : MessageObject) -> None:
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