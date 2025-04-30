from typing import Callable, Optional
from discord import Message
from enum import Enum, auto, unique
from classes.discord_lib import MessageObject
from classes.message_lib import ChannelObject
from classes.channel_enum import ChannelEnum

"""
ChannelMessageTemplate Usage Guide
----------------------------------

The `ChannelMessageTemplate` class provides a framework for creating and managing Discord bot commands 
within specific channels. It allows you to register commands, associate them with functions, and handle 
incoming messages to execute the appropriate command logic.

### Key Components:
1. **Command Registration**:
   - Use the `RegisterCommand` method to register a command with a unique `Enum` identifier and a `CommandObject`.
   - The `CommandObject` contains the command's name, description, and the function to execute.

2. **Command Setup**:
   - Call the `SetupCommand` method after registering all commands. This maps command names to their respective `Enum` identifiers.

3. **Channel Object Integration**:
   - Use the `ImportChannelObjectDict` method to associate the template with a dictionary of `ChannelObject` instances. 
   - This allows the template to access channel-specific configurations.

4. **Message Handling**:
   - The `ResMessage` method processes incoming messages. It extracts the command name from the message content, 
     looks up the corresponding function, and executes it.

5. **Function Execution**:
   - The `RunFunc` method is used internally to execute the function associated with a command. It passes the 
     `Message` and `MessageObject` instances to the function.

### Example Usage:
```python
from channel_template import ChannelMessageTemplate, CommandObject, CommandEnum
from discord import Message
from classes.discord_lib import MessageObject

# Define command functions
async def ResHelp(message: Message, message_object: MessageObject) -> None:
    message_object.SetMessage("Help Command Executed")

async def ResTest(message: Message, message_object: MessageObject) -> None:
    message_object.SetMessage("Test Command Executed")

# Create a template instance
channel_message_template = ChannelMessageTemplate()

# Register commands
channel_message_template.RegisterCommand(
    command_enum=CommandEnum.help_,
    command_object=CommandObject(name="help", description="Help Command", function=ResHelp)
)
channel_message_template.RegisterCommand(
    command_enum=CommandEnum.test_,
    command_object=CommandObject(name="test", description="Test Command", function=ResTest)
)

# Setup commands
channel_message_template.SetupCommand()

# Handle a message (example usage in an event handler)
async def on_message(message: Message):
    message_object = MessageObject()
    await channel_message_template.ResMessage(message=message, message_object=message_object)
    if not message_object.EmptyMessage():
        await message.channel.send(message_object.message_)
```

This template simplifies the process of managing commands and their execution, making it easier to extend and maintain the bot's functionality.
"""

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

class CommandObject():
    """
    The CommandObject class is used to store the command object.

    Attributes:
    name_ : str - The name of the command.
    description_ : str - The description of the command.
    function_ : Callable - The function of the command.

    Example:
    >>> command_object = CommandObject(name="help", description="Help Command", function=ResHelp)
    """
    def __init__(self, name : str, description : str, function : Callable) -> None:
        """
        Initialize the CommandObject class.

        Args:
        name : str - The name of the command.
        description : str - The description of the command.
        function : Callable - The function of the command.

        Attributes:
        name_ : str - The name of the command.
        description_ : str - The description of the command.
        function_ : Callable - The function of the command.

        Example:
        >>> command_object = CommandObject(name="help", description="Help Command", function=ResHelp)
        """
        self.name_ : str = name
        self.description_ : str = description
        self.function_ : Callable = function

class ChannelMessageTemplate():
    """
    This is a factory to create the ChannelMessage

    Attributes:
    command_object_dict_ : dict[Enum, CommandObject] - The dictionary containing the command objects.
    command_name_dict_ : dict[str, Enum] - The dictionary containing the command names.
    channel_object_dict_ : Optional[dict[Enum, ChannelObject]] - The dictionary containing the channel objects.

    Methods:
    RegisterCommand : Register the command for the ChannelMessageTemplate.
    SetupCommand : Setup the command for the ChannelMessageTemplate.
    ImportChannelObjectDict : Import the ChannelObject for the ChannelMessageTemplate
    RunFunc : Run the function for the ChannelMessageTemplate.
    ResMessage : Template for responding Messages

    Example:
    >>> class ChannelMessageDebug(ChannelMessageTemplate):
    >>>     pass
    """

    def __init__(self) -> None:
        """
        Initialize the ChannelMessageTemplate class.

        Attributes:
        command_object_dict_ : dict[Enum, CommandObject] - The dictionary containing the command objects.

        Example:
        >>> channel_message_template = ChannelMessageTemplate()
        """
        self.command_object_dict_ : dict[Enum, CommandObject] = {}
        self.command_name_dict_ : dict[str, Enum] = {}
        self.channel_object_dict_ : Optional[dict[Enum, ChannelObject]] = None


    def RegisterCommand(self, command_enum : Enum, command_object : CommandObject) -> None:
        """
        Register the command for the ChannelMessageTemplate.

        Args:
        command_enum : Enum - The Enum for the command.
        command_object : CommandObject - The CommandObject for the command.

        Example:
        >>> command_enum = CommandEnum.help_
        >>> command_object = CommandObject(name="help", description="Help Command", function=ResHelp)
        >>> channel_message_template = ChannelMessageTemplate()
        >>> channel_message_template.RegisterCommand(command_enum=command_enum, command_object=command_object)
        """
        self.command_object_dict_[command_enum] = command_object

    def SetupCommand(self) -> None:
        """
        Setup the command for the ChannelMessageTemplate.

        Example:
        >>> command_enum = CommandEnum.help_
        >>> command_object = CommandObject(name="help", description="Help Command", function=ResHelp)
        >>> channel_message_template = ChannelMessageTemplate()
        >>> channel_message_template.RegisterCommand(command_enum=command_enum, command_object=command_object)
        >>> channel_message_template.SetupCommand()
        """
        for command_enum, command_object in self.command_object_dict_.items():
            self.command_name_dict_[command_object.name_] = command_enum
        print(f"{self.__class__.__name__} Setup Done")

    def ImportChannelObjectDict(self, channel_object_dict : dict[Enum, ChannelObject]) -> None:
        """
        Import the ChannelObject for the ChannelMessageTemplate

        Args:
        channel_object_dict : dict[Enum, ChannelObject] - The dictionary containing the channel objects.

        Example:
        >>> channel_object_dict = {}
        >>> channel_message_template = ChannelMessageTemplate()
        >>> channel_message_template.ImportChannelObjectDict(channel_object_dict=channel_object_dict)
        """
        self.channel_object_dict_ = channel_object_dict

    async def RunFunc(self, *, func : Callable[[Message, MessageObject], None], message : Message, message_object : MessageObject) -> None:
        """
        Run the function for the ChannelMessageTemplate.

        Args:
        func : Callable[[Message, MessageObject], None] - The function to run.
        message : Message - The Message object.
        message_object : MessageObject - The MessageObject object.

        Example:
        >>> async def ResHelp(message : Message, message_object : MessageObject) -> None:
        >>>     message_object.SetMessage("Help Command")
        >>> command_enum = CommandEnum.help_
        >>> command_object = CommandObject(name="help", description="Help Command", function=ResHelp)
        >>> channel_message_template = ChannelMessageTemplate()
        >>> channel_message_template.RegisterCommand(command_enum=command_enum, command_object=command_object)
        >>> await channel_message_template.RunFunc(func=channel_message_template.command_object_dict_[command_enum].function_, message=message, message_object=message_object)
        """
        await func(message, message_object) # type: ignore

    async def ResMessage(self, message : Message, message_object : MessageObject) -> None:
        """
        Template for responding Messages
        """
        content : str = message.content[1:].split(" ")[0]
        if content in self.command_name_dict_:
            await self.RunFunc(func=self.command_object_dict_[self.command_name_dict_[content]].function_, message=message, message_object=message_object)
        else:
            message_object.SetMessage("Command not found")

# SAMPLE CODE
CHANNEL_MESSAGE_TEMPLATE : ChannelMessageTemplate = ChannelMessageTemplate()

async def ResHelp(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the help of the system
    """
    message_object.CreateEmbed(title="Help", description="Help Command")
    for command_enum, command_object in CHANNEL_MESSAGE_TEMPLATE.command_object_dict_.items():
        message_object.EmbedAddField(name=command_object.name_, value=command_object.description_)
    
async def ResTest(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system
    """
    message_object.SetMessage("Test Command :" + CHANNEL_MESSAGE_TEMPLATE.__class__.__name__)

def Setup() -> None:
    """
    Setup the ChannelMessageTemplate
    """
    CHANNEL_MESSAGE_TEMPLATE.RegisterCommand(
        command_enum=CommandEnum.help_, 
        command_object=CommandObject(
            name="help", 
            description="Help Command", 
            function=ResHelp))
    CHANNEL_MESSAGE_TEMPLATE.RegisterCommand(
        command_enum=CommandEnum.test_, 
        command_object=CommandObject(
            name="test", 
            description="Test Command", 
            function=ResTest))
    CHANNEL_MESSAGE_TEMPLATE.SetupCommand()