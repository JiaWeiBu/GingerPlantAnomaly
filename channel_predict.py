from aiohttp import ClientSession, FormData
from io import BytesIO
from discord import Message, File
from PIL.Image import open
from enum import Enum, auto, unique
from classes.discord_lib import MessageObject
from channel_template import ChannelMessageTemplate, CommandObject
from classes.util_lib import Unused
from classes.channel_enum import ChannelEnum
from classes.message_lib import WebhookSend
import base64


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
    predict_ = auto()
    setup_ = auto()

CHANNEL_MESSAGE_PREDICT : ChannelMessageTemplate = ChannelMessageTemplate()
async def ResPredict(message: Message, message_object: MessageObject) -> None:
    """
    This is used for the debug of the system

    This channel can access hidden commands for the system.

    This is a private channel for the system

    Train ANOMALIV
    """
    assert CHANNEL_MESSAGE_PREDICT.channel_object_dict_ is not None, "ChannelObjectDict is not set"
    
    if not message.attachments:
        message_object.SetMessage("No attachment found")

    form_data = FormData()
    for attachment in message.attachments:
        # Check if the attachment is an image
        if not attachment.content_type.startswith("image/"): # type: ignore
            continue

        file: File = await attachment.to_file()
        image = open(file.fp)  # type: ignore
        if not image:
            message_object.SetMessage("Failed to open the image.")
            return

        # Convert the image to bytes
        image_buffer = BytesIO()
        image.save(image_buffer, format=image.format)
        image_buffer.seek(0)

        # Add the image to the form data
        form_data.add_field(
            "images",
            image_buffer,
            filename=file.filename,
            content_type=attachment.content_type
        )
    
    # Validate if FormData is empty
    if not form_data._fields:  # _fields contains all the fields added to FormDatapart():
        message_object.SetMessage("No valid images found in the attachments.")
        return

    # Send all images to the server in one request
    url = "http://127.0.0.1:5000/predict"
    async with ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            if response.status != 200:
                # Check if the response is JSON
                if response.content_type == "application/json":
                    try:
                        error_result = await response.json()
                        error_messages = error_result.get("messages", [])
                        error_detail = "\n".join(error_messages)
                    except Exception:
                        error_detail = "Invalid JSON response from server."
                else:
                    error_detail = await response.text()  # Fallback to plain text

                message_object.SetMessage(f"Error {response.status}: {error_detail}")
                return

            # Check if the response is JSON
            if response.content_type == "application/json":
                try:
                    result = await response.json()
                except Exception:
                    message_object.SetMessage("Invalid JSON response from server.")
                    return
            else:
                result = {"messages": [], "images": []}  # Default empty result if not JSON

            response_messages = result.get("messages", [])
            images_base64 = result.get("images", [])

            if images_base64 is None or response_messages is None:
                message_object.SetMessage("No images or messages found in the response.")
                return

            if len(response_messages) == 1 and len(images_base64) == 1:
                # Single response case
                response_message = response_messages[0]
                processed_image_buffer = BytesIO(base64.b64decode(images_base64[0]))
                processed_image_buffer.seek(0)

                # Extract the score from the response_message
                try:
                    pred_score = float(response_message.split(":")[1].strip())
                except (IndexError, ValueError):
                    pred_score = None

                # Determine the anomaly level and set the title and color
                if pred_score is not None:
                    if pred_score > 0.7:
                        title = "Anomaly Detected"
                        colour = MessageObject.EmbedColourEnum.red_.value
                    elif pred_score > 0.5:
                        title = "Potential Anomaly"
                        colour = MessageObject.EmbedColourEnum.yellow_.value
                    elif pred_score > 0.3:
                        title = "Potential Normal"
                        colour = MessageObject.EmbedColourEnum.blue_.value
                    else:
                        title = "Normal"
                        colour = MessageObject.EmbedColourEnum.green_.value
                else:
                    title = "Prediction"
                    colour = MessageObject.EmbedColourEnum.random_.value

                # Set the file in the message object
                message_object.SetFile(
                    fp=processed_image_buffer,
                    filename="processed_image.png",
                    description="Processed image"
                )

                # Create an embed with the response
                message_object.CreateEmbed(
                    title=title,
                    description=response_message,
                    colour=colour
                )

                # Attach the image to the embed
                message_object.EmbedSetImage(url="attachment://processed_image.png")
            else:
                # Multiple responses case
                webhook_url = CHANNEL_MESSAGE_PREDICT.channel_object_dict_[ChannelEnum.predict_].webhook_url_
                for response_message, image_base64 in zip(response_messages, images_base64):
                    processed_image_buffer = BytesIO(base64.b64decode(image_base64))
                    processed_image_buffer.seek(0)

                    # Extract the score from the response_message
                    try:
                        pred_score = float(response_message.split(":")[1].strip())
                    except (IndexError, ValueError):
                        pred_score = None

                    # Determine the anomaly level and set the title and color
                    if pred_score is not None:
                        if pred_score > 0.7:
                            title = "Anomaly Detected"
                            colour = MessageObject.EmbedColourEnum.red_.value
                        elif pred_score > 0.5:
                            title = "Potential Anomaly"
                            colour = MessageObject.EmbedColourEnum.yellow_.value
                        elif pred_score > 0.3:
                            title = "Potential Normal"
                            colour = MessageObject.EmbedColourEnum.blue_.value
                        else:
                            title = "Normal"
                            colour = MessageObject.EmbedColourEnum.green_.value
                    else:
                        title = "Prediction"
                        colour = MessageObject.EmbedColourEnum.random_.value

                    # Create a new message object for each response
                    new_message_object = MessageObject()
                    new_message_object.SetFile(
                        fp=processed_image_buffer,
                        filename="processed_image.png",
                        description="Processed image"
                    )
                    new_message_object.CreateEmbed(
                        title=title,
                        description=response_message,
                        colour=colour
                    )
                    new_message_object.EmbedSetImage(url="attachment://processed_image.png")

                    # Send the message object via webhook
                    await WebhookSend(webhook_url=webhook_url, message_object=new_message_object)

                # Leave the original message object blank
                if not message_object.EmptyMessage():
                    message_object.ClearMessage()

async def ResSetup(message: Message, message_object: MessageObject) -> None:
    """
    This is used for the setup model for predict.
    """
    # Extract content and split into words
    content_parts = message.content.split()
    if len(content_parts) != 3:
        message_object.SetMessage("Invalid command format. Use: {command} {model} {week}")
        return

    command, part1, part2 = content_parts

    # Determine which part is the model and which is the week
    model = None
    week = None
    try:
        week = int(part1)
        model = part2
    except ValueError:
        try:
            week = int(part2)
            model = part1
        except ValueError:
            message_object.SetMessage("Invalid format. Ensure one part is a model (string) and the other is a week (integer).")
            return

    # Prepare the form data for the server
    form_data = FormData()
    form_data.add_field("week", str(week))
    form_data.add_field("name", model)

    # Send the setup request to the server
    url = "http://127.0.0.1:5000/predict_setup"
    async with ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            if response.status != 200:
                error_detail = await response.text()  # Await the coroutine
                message_object.SetMessage(f"Error: {response.status} - {error_detail}")
                return

            # Check if the response is JSON
            if response.content_type == "application/json":
                result = await response.json()
            else:
                result = await response.text()

            message_object.SetMessage(f"Setup successful: {result}")

async def ResHelp(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the help of the system
    """
    Unused(message)
    message_object.CreateEmbed(title="Help", description="Help Command")
    for command_object in CHANNEL_MESSAGE_PREDICT.command_object_dict_.values():
        message_object.EmbedAddField(name=command_object.name_, value=command_object.description_)
    
async def ResTest(message : Message, message_object : MessageObject) -> None:
    """
    This is used for the test of the system
    """
    message_object.SetMessage("Predict : " + message.content)

def Setup() -> None:
    """
    Setup the ChannelMessageTemplate
    """
    CHANNEL_MESSAGE_PREDICT.RegisterCommand(
        command_enum=CommandEnum.help_, 
        command_object=CommandObject(
            name="help", 
            description="Help Command", 
            function=ResHelp))
    CHANNEL_MESSAGE_PREDICT.RegisterCommand(
        command_enum=CommandEnum.test_, 
        command_object=CommandObject(
            name="test", 
            description="Test Command", 
            function=ResTest))
    CHANNEL_MESSAGE_PREDICT.RegisterCommand(
        command_enum=CommandEnum.predict_, 
        command_object=CommandObject(
            name="predict", 
            description="Predict Command", 
            function=ResPredict))
    CHANNEL_MESSAGE_PREDICT.RegisterCommand(
        command_enum=CommandEnum.setup_, 
        command_object=CommandObject(
            name="setup", 
            description="Setup Command", 
            function=ResSetup))
    CHANNEL_MESSAGE_PREDICT.SetupCommand()