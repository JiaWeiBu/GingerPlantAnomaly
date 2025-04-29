# Discord Bot UI

[Back to Main README](./README.md)

## Overview
This project includes a Discord bot implementation designed to provide an interactive user interface for managing anomaly detection tasks. The bot is implemented using Object-Oriented Programming (OOP) principles, ensuring modularity and scalability.

## Features
- **Command-Based Interaction**: Users can interact with the bot using predefined commands.
- **Customizable Command Rooms**: Each server chat room can act as a separate command room with its own set of commands.
- **Dynamic Responses**: The bot dynamically responds to user inputs based on the registered commands.
- **Extensible Design**: New commands and functionalities can be easily added using the `channel_template.py` factory.

## How It Works
1. **Command Registration**:
   - Commands are registered using the `ChannelMessageTemplate` class in `channel_template.py`.
   - Each command is associated with a name, description, and a function to execute.

2. **Command Execution**:
   - When a user sends a command in the chat, the bot parses the command and executes the corresponding function.
   - If the command is not recognized, the bot responds with a "Command not found" message.

3. **Channel-Specific Commands**:
   - Each chat room can have its own set of commands, allowing for server-specific customization.
   - This is achieved by creating instances of `ChannelMessageTemplate` for each chat room.

## Example Commands
- **Help Command**:
  - Command: `!help`
  - Description: Displays a list of available commands and their descriptions.
  - Implementation: The `ResHelp` function in `channel_template.py`.

- **Test Command**:
  - Command: `!test`
  - Description: A test command to verify the bot's functionality.
  - Implementation: The `ResTest` function in `channel_template.py`.

## File Structure
- **`channel_template.py`**:
  - Acts as a factory for creating and managing command rooms.
  - Provides methods for registering commands, setting up commands, and handling user interactions.

- **`classes/discord_lib.py`**:
  - Contains utility classes for managing Discord-specific functionalities, such as sending messages and creating embeds.

- **`classes/message_lib.py`**:
  - Provides helper classes for managing message objects and their attributes.

## Setting Up the Bot
1. **Create a Discord Bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application and generate a bot token.

2. **Configure the Bot**:
   - Add the bot token to your environment variables or configuration file.
   - Invite the bot to your server using the OAuth2 URL.

3. **Run the Bot**:
   - Start the bot by running the main script:
     ```bash
     python bot_main.py
     ```

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

## Notes
- The bot is designed to handle multiple servers and chat rooms efficiently.
- Ensure that the bot has the necessary permissions to read and send messages in the designated channels.
