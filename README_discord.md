# Discord Bot UI

[Back to Main README](./README.md)

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [How It Works](#how-it-works)
   - [Command Registration](#command-registration)
   - [Command Execution](#command-execution)
   - [Channel-Specific Commands](#channel-specific-commands)
4. [Key Components](#key-components)
   - [ChannelMessageTemplate](#channelmessagetemplate)
   - [MessageObject](#messageobject)
   - [MessageUnit](#messageunit)
   - [discord_lib as a Facade](#discord_lib-as-a-facade)
5. [Setting Up the Bot](#setting-up-the-bot)
   - [Environment Variables](#environment-variables)
   - [Webhook Links](#webhook-links)
   - [Keyword and Initialization Phrase](#keyword-and-initialization-phrase)
6. [Extending the Bot](#extending-the-bot)
7. [Notes](#notes)

---

## Overview
This project includes a Discord bot implementation designed to provide an interactive user interface for managing anomaly detection tasks. The bot is implemented using Object-Oriented Programming (OOP) principles, ensuring modularity and scalability.

---

## Features
- **Command-Based Interaction**: Users can interact with the bot using predefined commands.
- **Customizable Command Rooms**: Each server chat room can act as a separate command room with its own set of commands.
- **Dynamic Responses**: The bot dynamically responds to user inputs based on the registered commands.
- **Extensible Design**: New commands and functionalities can be easily added using the `channel_template.py` factory.

---

## How It Works

### Command Registration
Commands are registered using the `ChannelMessageTemplate` class in `channel_template.py`. Each command is associated with:
- A unique `Enum` identifier.
- A `CommandObject` containing:
  - The command's name.
  - A description.
  - A function to execute.

Example:
```python
CHANNEL_MESSAGE_TEMPLATE.RegisterCommand(
    command_enum=CommandEnum.help_,
    command_object=CommandObject(
        name="help",
        description="Help Command",
        function=ResHelp
    )
)
```

### Command Execution
When a user sends a command in the chat:
1. The bot parses the command.
2. It matches the command name with the registered commands.
3. The corresponding function is executed.
4. If the command is not recognized, the bot responds with "Command not found."

### Channel-Specific Commands
Each chat room can have its own set of commands, allowing for server-specific customization. This is achieved by creating instances of `ChannelMessageTemplate` for each chat room.

---

## Key Components

### ChannelMessageTemplate
This is the core factory for creating and managing commands. It provides methods to:
- Register commands (`RegisterCommand`).
- Map command names to their `Enum` identifiers (`SetupCommand`).
- Handle incoming messages and execute the appropriate command (`ResMessage`).

### MessageObject
`MessageObject` acts as a container for Discord messages, embeds, and files. It simplifies the process of constructing and sending messages.

Key Features:
- **SetMessage**: Sets the plain text message.
- **CreateEmbed**: Creates an embed with a title, description, and optional fields.
- **SetFile**: Attaches a file to the message.

Example:
```python
message_object = MessageObject()
message_object.SetMessage("Hello, World!")
message_object.CreateEmbed(title="Greetings", description="This is an example embed.")
```

### MessageUnit
`MessageUnit` manages the interaction between channels and their respective commands. It:
1. Registers channels and their callback functions.
2. Validates incoming messages based on the channel and keyword.
3. Routes messages to the appropriate command function.

### discord_lib as a Facade
The `discord_lib.py` file acts as a facade to the Discord library. It abstracts away the complexity of Discord's API and provides a simplified interface for:
- Creating and managing embeds.
- Sending messages and files.
- Handling Discord-specific objects like `Message` and `Embed`.

---

## Setting Up the Bot

### Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
TOKEN_BOT_GITHUB=<your-bot-token>
CHANNEL_WEBHOOK_LOG=<webhook-url-for-log-channel>
CHANNEL_WEBHOOK_PREDICT=<webhook-url-for-predict-channel>
CHANNEL_WEBHOOK_DEBUG=<webhook-url-for-debug-channel>
CHANNEL_WEBHOOK_CLONE=<webhook-url-for-clone-channel>
```

### Webhook Links
Each channel requires a webhook URL for sending messages. These URLs should be added to the `.env` file as shown above.

### Keyword and Initialization Phrase
- **Keyword**: The bot listens for messages starting with a specific keyword. This is defined in `channel.py` as `CHANNEL_KEYWORD`.
- **Initialization Phrase**: The bot uses an initialization phrase (`INIT_PHRASE`) to set up channel IDs. This is defined in `message_lib.py`.

---

## Extending the Bot
To add new commands:
1. Define a new function for the command.
2. Register the command using the `RegisterCommand` method in `channel_template.py`.
3. Add the command to the `Setup` function for initialization.

Example:
```python
async def ResNewCommand(message: Message, message_object: MessageObject) -> None:
    message_object.SetMessage("This is a new command!")

CHANNEL_MESSAGE_TEMPLATE.RegisterCommand(
    command_enum=CommandEnum.new_command_,
    command_object=CommandObject(
        name="new_command",
        description="A new custom command",
        function=ResNewCommand
    )
)
```

---

## Notes
- The bot is designed to handle multiple servers and chat rooms efficiently.
- Ensure that the bot has the necessary permissions to read and send messages in the designated channels.
- The `discord_lib.py` file simplifies interaction with Discord's API, making it easier to extend and maintain the bot's functionality.

---

## How `channel_template.py` Acts as a Factory

The `ChannelMessageTemplate` class in `channel_template.py` acts as a factory for creating and managing channels with their own set of commands. This design allows for modular and reusable channel-specific logic.

### Key Features of the Factory Design:
1. **Command Registration**:
   - Each channel can register its own commands using the `RegisterCommand` method.
   - Commands are associated with a unique `Enum` identifier and a `CommandObject` containing the command's name, description, and function.

2. **Command Setup**:
   - After registering commands, the `SetupCommand` method maps command names to their respective `Enum` identifiers, enabling efficient lookup and execution.

3. **Channel-Specific Logic**:
   - Each channel can have its own instance of `ChannelMessageTemplate`, allowing for independent command handling and customization.

4. **Integration with Channel Objects**:
   - The `ImportChannelObjectDict` method integrates the template with a dictionary of `ChannelObject` instances, enabling access to channel-specific configurations like webhook URLs and IDs.

### Example: Creating a New Channel with Commands
To create a new channel with commands:
1. Define a new `Enum` class for the channel's commands.
2. Create an instance of `ChannelMessageTemplate`.
3. Register commands using `RegisterCommand`.
4. Set up the commands using `SetupCommand`.

Example:
```python
from channel_template import ChannelMessageTemplate, CommandObject
from enum import Enum, auto
from discord import Message
from classes.discord_lib import MessageObject

# Define command identifiers
class MyChannelCommands(Enum):
    greet = auto()
    farewell = auto()

# Create a new channel template
MY_CHANNEL_TEMPLATE = ChannelMessageTemplate()

# Define command functions
async def ResGreet(message: Message, message_object: MessageObject) -> None:
    message_object.SetMessage("Hello, welcome to the channel!")

async def ResFarewell(message: Message, message_object: MessageObject) -> None:
    message_object.SetMessage("Goodbye, see you next time!")

# Register commands
MY_CHANNEL_TEMPLATE.RegisterCommand(
    command_enum=MyChannelCommands.greet,
    command_object=CommandObject(
        name="greet",
        description="Greet the user",
        function=ResGreet
    )
)
MY_CHANNEL_TEMPLATE.RegisterCommand(
    command_enum=MyChannelCommands.farewell,
    command_object=CommandObject(
        name="farewell",
        description="Say goodbye to the user",
        function=ResFarewell
    )
)

# Set up commands
MY_CHANNEL_TEMPLATE.SetupCommand()
```

### Benefits of the Factory Design:
- **Modularity**: Each channel can have its own isolated logic and commands.
- **Reusability**: The same `ChannelMessageTemplate` class can be reused to create multiple channels with different commands.
- **Scalability**: Adding new channels or commands is straightforward and does not affect existing functionality.

This factory design ensures that the bot remains organized and easy to maintain as new channels and commands are added.
