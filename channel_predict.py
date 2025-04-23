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
        if not attachment.content_type.startswith("image/"):
            continue

        file: File = await attachment.to_file()
        image = open(file.fp)

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

    # Send all images to the server in one request
    url = "http://127.0.0.1:5000/predict"
    async with ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            if response.status != 200:
                message_object.SetMessage(f"Error: {response.status}")

            # Parse the response
            result = await response.json()
            response_messages = result.get("messages", [])
            images_base64 = result.get("images", [])

            if len(response_messages) == 1 and len(images_base64) == 1:
                # Single response case
                response_message = response_messages[0]
                processed_image_buffer = BytesIO(base64.b64decode(images_base64[0]))
                processed_image_buffer.seek(0)

                # Set the file in the message object
                message_object.SetFile(
                    fp=processed_image_buffer,
                    filename="processed_image.png",
                    description="Processed image"
                )

                # Create an embed with the response
                message_object.CreateEmbed(
                    title="Prediction",
                    description=response_message,
                    colour=MessageObject.EmbedColourEnum.random_.value
                )

                # Attach the image to the embed
                message_object.EmbedSetImage(url="attachment://processed_image.png")
            else:
                # Multiple responses case
                webhook_url = CHANNEL_MESSAGE_PREDICT.channel_object_dict_[ChannelEnum.predict_].webhook_url_
                for response_message, image_base64 in zip(response_messages, images_base64):
                    processed_image_buffer = BytesIO(base64.b64decode(image_base64))
                    processed_image_buffer.seek(0)

                    # Create a new message object for each response
                    new_message_object = MessageObject()
                    new_message_object.SetFile(
                        fp=processed_image_buffer,
                        filename="processed_image.png",
                        description="Processed image"
                    )
                    new_message_object.CreateEmbed(
                        title="Prediction",
                        description=response_message,
                        colour=MessageObject.EmbedColourEnum.random_.value
                    )
                    new_message_object.EmbedSetImage(url="attachment://processed_image.png")

                    # Send the message object via webhook
                    await WebhookSend(webhook_url=webhook_url, message_object=new_message_object)

                # Leave the original message object blank
                if not message_object.EmptyMessage():
                    message_object.ClearMessage()

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
    CHANNEL_MESSAGE_PREDICT.SetupCommand()