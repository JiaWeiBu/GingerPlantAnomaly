# self implement logging
# default prebuilt logging - create new file for each run
# custom logging - create discord thread for each run and log to that thread

# Criteria:
# - Use of classes
# - able to add new implementations
from typing import Optional
from enum import Enum, auto
from discord import Thread, Message
from classes.message_lib import WebhookSend
from classes.discord_lib import MessageObject

class LoggerTypeEnum(Enum):
    """
    Enum class for the logger types

    Attributes:
    default_ : Default logger type
    file_ : File logger type
    discord_ : Discord logger type
    """
    default_ = auto()
    file_ = auto()
    discord_ = auto()

class LoggerTemplate:
    """
    The LoggerTemplate class is used to create a template for logging.
    It can be used as a print function.

    Methods:
    Open : open the logger
    Output : output the text
    Close : close the logger

    Example:
    >>> logger = LoggerTemplate()
    >>> logger.Output(text="Hello World")
    """
    def __init__(self) -> None:
        ...

    def Open(self, **kwargs) -> None:
        ...
    
    def Output(self, **kwargs) -> None:
        """
        print the text to the console

        Args:
        text : str - the text to print

        Example:
        >>> logger = LoggerTemplate()
        >>> logger.Output(text="Hello World")
        """
        assert "text" in kwargs, "text is not in kwargs"
        print(kwargs["text"])

    def Close(self) -> None:
        ...

class AsyncLoggerTemplate:
    """
    The AsyncLoggerTemplate class is used to create a template for logging.
    It can be used as a async print function.

    Methods:
    Open : open the logger
    Output : output the text
    Close : close the logger

    Example:
    >>> logger = AsyncLoggerTemplate()
    >>> await logger.Output(text="Hello World")
    """
    def __init__(self) -> None:
        ...

    async def Open(self, **kwargs) -> None:
        ...

    async def Output(self, **kwargs) -> None:
        """
        print the text to the console

        Args:
        text : str - the text to print

        Example:
        >>> logger = AsyncLoggerTemplate()
        >>> await logger.Output(text="Hello World")
        """
        assert "text" in kwargs, "text is not in kwargs"
        print(kwargs["text"])

    async def Close(self) -> None:
        ...

class LoggerFile(LoggerTemplate):
    """
    The LoggerFile class is used to create a file logger.

    Attributes:
    file_ : file - the file object
    open_ : bool - the open status of the file

    Methods:
    Open : open the file
    Output : output the text
    Close : close the file

    Example:
    >>> logger = LoggerFile()
    >>> logger.Open(file_name="log.txt", modes="w")
    >>> logger.Output(text="Hello World")
    >>> logger.Close()
    """
    def __init__(self) -> None:
        self.file_ = None
        self.open_ : bool = False

    def Open(self, **kwargs) -> None:
        """
        Open the file for writing

        Args:
        file_name : str - the name of the file
        modes : str - the mode to open the file

        Example:
        >>> logger = LoggerFile()
        >>> logger.Open(file_name="log.txt", modes="w")
        """
        assert "file_name" in kwargs, "file_name is not in kwargs"
        assert "modes" in kwargs, "modes is not in kwargs"
        file_name = kwargs["file_name"]
        modes = kwargs["modes"]
        assert isinstance(file_name, str), "file_name is not a string"
        assert isinstance(modes, str), "modes is not a string"
        assert modes in ["w", "a","r"], "modes is not 'w' or 'a' or 'r'"
        assert not self.open_, "File is already open"
        self.file_ = open(kwargs["file_name"], kwargs["modes"])
        self.open_ = True

    def Output(self, **kwargs) -> None:
        """
        Write the text to the file

        Args:
        text : str - the text to write

        Example:
        >>> logger = LoggerFile("log.txt")
        >>> logger.Open(file_name="log.txt", modes="w")
        >>> logger.Output(text="Hello World")
        >>> logger.Close()
        """
        assert self.open_, "File is not open"
        assert "text" in kwargs, "text is not in kwargs"
        text = kwargs["text"]
        assert isinstance(text, str), "text is not a string"
        self.file_.write(text) # type: ignore

    def Close(self) -> None:
        """
        Close the file

        Example:
        >>> logger = LoggerFile("log.txt")
        >>> logger.Open(file_name="log.txt", modes="w")
        >>> logger.Output(text="Hello World")
        >>> logger.Close()
        """
        assert self.open_, "File is not open"
        self.file_.close() # type: ignore
        self.open_ = False

class LoggerDiscord(AsyncLoggerTemplate):
    """
    The LoggerDiscord class is used to create a discord logger.

    Attributes:
    thread_ : Thread - the thread object

    Methods:
    Setup : setup the logger
    Open : open the thread
    Output : output the text
    Close : close the thread

    Example:
    >>> logger = LoggerDiscord()
    >>> await logger.Setup(webhook_link="https://discord.com/api/webhooks/...")
    >>> await logger.Open(message=message, name="Log Thread", duration=1440)
    >>> await logger.Output(message_object=message_object)
    >>> await logger.Close()
    """
    def __init__(self) -> None:
        self.thread_ : Optional[Thread] = None

    async def Setup(self, webhook_link : str, name : str) -> None:
        """
        Setup the logging by sending a webhook

        NOTE requires external to open the thread and link the message to it

        Args:
        webhook_link : str - the discord webhook link
        name : str - the name of the thread

        Example:
        >>> logger = LoggerDiscord()
        >>> await logger.Setup(webhook_link="https://discord.com/api/webhooks/...")
        """
        await WebhookSend(webhook_url=webhook_link, content=name)
    
    async def Open(self, **kwargs) -> None:
        """
        Create a thread for logging to discord

        NOTE requires external to link the message to the thread

        Args:
        message : Message - the message information to create the thread
        name : str - the name of the thread
        duration : int - the duration of the thread to auto archive

        Example:
        >>> logger = LoggerDiscord()
        >>> await logger.Open(message=message, name="Log Thread", duration=1440)
        """
        assert "message" in kwargs, "message is not in kwargs"
        assert "name" in kwargs, "name is not in kwargs"
        assert "duration" in kwargs, "duration is not in kwargs"
        message = kwargs["message"]
        name = kwargs["name"]
        duration = kwargs["duration"]
        assert isinstance(message, Message), "message is not a Message"
        assert isinstance(name, str), "name is not a string"
        assert duration in [60, 1440, 4320, 10080], "duration is not in [60, 1440, 4320, 10080]"

        await message.create_thread(name=name, auto_archive_duration=duration)
        assert message.thread is not None, "Thread is empty"
        self.thread_ = message.thread

    async def Output(self, **kwargs) -> None:
        """
        Send a message to the thread

        Args:
        message_object : MessageObject - the message information to send

        Example:
        >>> logger = LoggerDiscord()
        >>> await logger.Open(message=message, name="Log Thread", duration=1440)
        >>> await logger.Output(message_object=message_object)
        >>> await logger.Close()
        """
        assert self.thread_ is not None, "Thread is not created"
        
        # kwargs contains message_object
        assert "message_object" in kwargs, "message_object is not in kwargs"
        message_object : MessageObject = kwargs["message_object"]
        assert isinstance(message_object, MessageObject), "message_object is not a MessageObject"
        await self.thread_.send(message_object.message_, embed=message_object.embed_, file=message_object.file_) # type: ignore

    async def Close(self) -> None:
        """
        Close the thread

        Example:
        >>> logger = LoggerDiscord()
        >>> await logger.Open(message=message, name="Log Thread", duration=1440)
        >>> await logger.Output(message_object=message_object)
        >>> await logger.Close()
        """
        self.thread_ = None