# Discord Bot UI

[Back to Main README](./README.md)

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [How It Works](#how-it-works)
4. [Key Components](#key-components)
5. [Setting Up the Bot](#setting-up-the-bot)
   - [Creating a Discord Application](#creating-a-discord-application)
   - [Creating Webhooks](#creating-webhooks)
   - [Creating and Inviting the Bot](#creating-and-inviting-the-bot)
   - [Setting the Bot Token](#setting-the-bot-token)
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

### Creating a Discord Application
1. Go to the [Discord Developer Portal](https://discord.com/developers/docs/intro).
2. Log in with your Discord account.
3. Click on the **"New Application"** button.
4. Enter a name for your application and click **"Create"**.
5. Navigate to the **"Bot"** tab in the left-hand menu.
6. Click **"Add Bot"** and confirm by clicking **"Yes, do it!"**.
7. Copy the **Token** for your bot. This will be used in the `.env` file as `TOKEN_BOT_GITHUB`.

### Creating Webhooks
1. Open your Discord server and navigate to the channel where you want to create a webhook.
2. Click on the channel name and select **"Edit Channel"**.
3. Go to the **"Integrations"** tab and click **"Create Webhook"**.
4. Set a name and optionally an avatar for the webhook.
5. Copy the **Webhook URL** and save it. This will be used in the `.env` file as:
   - `CHANNEL_WEBHOOK_LOG`
   - `CHANNEL_WEBHOOK_PREDICT`
   - `CHANNEL_WEBHOOK_DEBUG`
   - `CHANNEL_WEBHOOK_CLONE`

For more details, refer to the [Discord Webhooks Guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

### Creating and Inviting the Bot
1. In the [Discord Developer Portal](https://discord.com/developers/docs/intro), go to your application.
2. Navigate to the **"OAuth2"** tab and select **"URL Generator"**.
3. Under **Scopes**, select **"bot"**.
4. Under **Bot Permissions**, select the permissions your bot needs (e.g., **"Send Messages"**, **"Read Messages"**, etc.).
5. Copy the generated URL and paste it into your browser.
6. Select the server where you want to add the bot and click **"Authorize"**.

For more details, refer to the [Discord.py Bot Guide](https://discordpy.readthedocs.io/en/stable/discord.html).

### Setting the Bot Token
1. Open the `.env` file in the root directory of the project.
2. Add the following line to set the bot token:
   ```env
   TOKEN_BOT_GITHUB=<your-bot-token>
   ```
3. Replace `<your-bot-token>` with the token you copied from the [Discord Developer Portal](https://discord.com/developers/docs/intro).

**Note**: The `TOKEN_BOT_GITHUB` is used by the bot to authenticate and connect to Discord. Ensure this token is kept secure and not shared publicly.

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
