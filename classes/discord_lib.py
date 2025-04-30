from typing import Optional, Union, Any
from os import PathLike
from io import BufferedIOBase
from enum import Enum, unique
from discord import Embed, Colour, File
from datetime import datetime

class MessageObject:
    """
    Class for the message object

    Attributes:
    - embed_: The embed object
    - message_: The message to be sent
    - file_: The file object to be sent

    Methods:
    - EmptyMessage: Check if the message object is empty
    - ClearMessage: Clear the message object
    
    Setters:
    - SetMessage: Set the message for the message object
    - CreateEmbed: Create an embed object
    - EmbedSetFooter: Set the footer for the embed
    - EmbedAddField: Add a field to the embed
    - EmbedSetImage: Set the image for the embed
    - EmbedSetThumbnail: Set the thumbnail for the embed
    - SetFile: Set the file object for the message

    Getters:
    - GetMessage: Get the message
    - GetEmbed: Get the embed object
    - GetFile: Get the file object

    TODO:
    - Discord allows a maximum of 10 embeds per message. The current implementation does not handle this limitation.
      Future upgrades may require splitting messages or managing multiple embeds.

    Example:
    >>> message_object_ = MessageObject()
    >>> message_object_.SetMessage("Hello World")
    >>> discord_message : str = message_object_.GetMessage()
    >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
    >>> embed_object : Embed = message_object_.GetEmbed()
    >>> message_object_.SetFile(fp="image.jpg", filename="image.jpg", description="This is an image")
    >>> file_object : File = message_object_.GetFile()
    """

    class EmbedColourEnum(Enum):
        """
        Enum class for the colours of the embeds

        Attributes:
        - blue_: Blue colour
        - blurple_: Blurple colour
        - brand_green_: Brand green colour
        - brand_red_: Brand red colour
        - dark_blue_: Dark blue colour
        - dark_embed_: Dark embed colour
        - dark_gold_: Dark gold colour
        - dark_gray_: Dark gray colour
        - dark_green_: Dark green colour
        - dark_grey_: Dark grey colour
        - dark_magenta_: Dark magenta colour
        - dark_orange_: Dark orange colour
        - dark_purple_: Dark purple colour
        - dark_red_: Dark red colour
        - dark_teal_: Dark teal colour
        - dark_theme_: Dark theme colour
        - darker_grey_: Darker grey colour
        - default_: Default colour
        - fuchsia_: Fuchsia colour
        - gold_: Gold colour
        - green_: Green colour
        - greyple_: Greyple colour
        - light_embed_: Light embed colour
        - light_grey_: Light grey colour
        - lighter_grey_: Lighter grey colour
        - magenta_: Magenta colour
        - og_blurple_: OG Blurple colour
        - orange_: Orange colour
        - pink_: Pink colour
        - purple_: Purple colour
        - random_: Random colour
        - red_: Red colour
        - teal_: Teal colour
        - yellow_: Yellow colour
        """
        blue_ = Colour.blue()
        blurple_ = Colour.blurple()
        brand_green_ = Colour.brand_green()
        brand_red_ = Colour.brand_red()
        dark_blue_ = Colour.dark_blue()
        dark_embed_ = Colour.dark_embed()
        dark_gold_ = Colour.dark_gold()
        dark_gray_ = Colour.dark_grey()
        dark_green_ = Colour.dark_green()
        dark_grey_ = Colour.dark_grey()
        dark_magenta_ = Colour.dark_magenta()
        dark_orange_ = Colour.dark_orange()
        dark_purple_ = Colour.dark_purple()
        dark_red_ = Colour.dark_red()
        dark_teal_ = Colour.dark_teal()
        dark_theme_ = Colour.dark_theme()
        darker_grey_ = Colour.darker_grey()
        default_ = Colour.default()
        fuchsia_ = Colour.fuchsia()
        gold_ = Colour.gold()
        green_ = Colour.green()
        greyple_ = Colour.greyple()
        light_embed_ = Colour.light_embed()
        light_grey_ = Colour.light_grey()
        lighter_grey_ = Colour.lighter_grey()
        magenta_ = Colour.magenta()
        og_blurple_ = Colour.og_blurple()
        orange_ = Colour.orange()
        pink_ = Colour.pink()
        purple_ = Colour.purple()
        random_ = Colour.random()
        red_ = Colour.red()
        teal_ = Colour.teal()
        yellow_ = Colour.yellow()

    def __init__(self) -> None:
        """
        Constructor for the MessageObject class

        Attributes:
        - embed_: The embed object
        - message_: The message to be sent
        - file_: The file object to be sent

        Example:
        >>> message_object_ = MessageObject()
        """
        self.embed_ : Optional[Embed] = None
        self.message_ : Optional[str] = None
        self.file_ : Optional[File] = None

    def EmptyMessage(self) -> bool:
        """
        Check if the message object is empty

        Returns:
        - True if the message object is empty, False otherwise

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetMessage("Hello World")
        >>> discord_message : str = message_object_.GetMessage()
        False
        """
        toggle : bool = False
        if self.message_ is None and self.embed_ is None and self.file_ is None:
            toggle = True
        return toggle

    def ClearMessage(self) -> None:
        """
        Clear the message object

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetMessage("Hello World")
        >>> discord_message : str = message_object_.GetMessage()
        >>> message_object_.ClearMessage()
        >>> discord_message : str = message_object_.GetMessage()
        """
        self.embed_ = None
        self.message_ = None
        self.file_ = None

    # Setters
    def SetMessage(self, message: str) -> None:
        """
        Set the message for the message object

        Args:
        - message: The message to be sent

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetMessage("Hello World")
        >>> discord_message : str = message_object_.GetMessage()
        """
        self.message_ = message

    def CreateEmbed(self, title : Optional[str] = None, description : Optional[str] = None, colour : Colour = Colour.default(), url : Optional[str] = None, timestamp : datetime = datetime.now()) -> None:
        """
        Create an embed object

        Args:
        - title: The title of the embed
        - description: The description of the embed
        - colour: The colour of the embed
        - url: The URL of the embed
        - timestamp: The timestamp of the embed

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        """
        self.embed_ = Embed(title = title, description = description, colour = colour, url = url, timestamp = timestamp)

    def EmbedSetFooter(self, *, text : str, icon_url : str | None = None) -> None:
        """
        Set the footer for the embed

        Args:
        - text: The text of the footer
        - icon_url: The URL of the icon

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        >>> message_object_.EmbedSetFooter(text="Footer Text", icon_url="https://example.com/icon.png")
        """
        assert self.embed_ is not None, "Embed object is not created yet"
        self.embed_.set_footer(text=text, icon_url=icon_url)

    def EmbedAddField(self, *, name : str, value : str, inline : bool = True) -> None: 
        """
        Add a field to the embed

        Args:
        - name: The name of the field
        - value: The value of the field
        - inline: Whether the field is inline or not

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        >>> message_object_.EmbedAddField(name="Field Name", value="Field Value")
        """
        assert self.embed_ is not None, "Embed object is not created yet"
        self.embed_.add_field(name=name, value=value, inline=inline)
    
    def EmbedSetImage(self, url : str) -> None:
        """
        Set the image for the embed

        Args:
        - url: The URL of the image

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetFile(fp="image.jpg", filename="image.jpg", description="This is an image")
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        >>> message_object_.EmbedSetImage(url="attachment://image.jpg")
        """
        assert self.embed_ is not None, "Embed object is not created yet"
        self.embed_.set_image(url=url)
    
    def EmbedSetThumbnail(self, url : str) -> None:
        """
        Set the thumbnail for the embed

        Args:
        - url: The URL of the thumbnail

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        >>> message_object_.EmbedSetThumbnail(url="https://example.com/thumbnail.png")
        """
        assert self.embed_ is not None, "Embed object is not created yet"
        self.embed_.set_thumbnail(url=url)

    def SetFile(self, fp : Union[str, bytes, PathLike[Any], BufferedIOBase], *, filename : Optional[str] = None, description : Optional[str] = None, spoiler : bool = False) -> None:
        """
        Set the file object for the message
        Image, video, etc. can be sent using this method

        Args:
        - fp: Filename or binary mode file-like object representing the file 
        - filename: The name of the file display in Discord
        - description: The description of the file (Only Images)
        - spoiler: Whether the file is a spoiler or not

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetFile(fp="image.jpg", filename="image.jpg", description="This is an image")
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        >>> message_object_.EmbedSetImage(url="attachment://image.jpg")
        """
        self.file_ = File(fp, filename = filename, description = description, spoiler = spoiler)

    # Getters
    def GetMessage(self) -> Optional[str]:
        """
        Get the message

        Returns:
        - The message to be sent
        
        NOTE
        - If the message is not set, it will return None
        - None is intended so that discord will treat it as no message to be sent

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetMessage("Hello World")
        >>> discord_message : str = message_object_.GetMessage()
        """
        return self.message_

    def GetEmbed(self) -> Optional[Embed]:
        """
        Get the embed object

        Returns:
        - The embed object

        NOTE
        - If the embed object is not created, it will return None
        - None is intended so that discord will treat it as no embed to be sent

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.CreateEmbed(title="Hello World", description="This is a test message")
        >>> embed_object : Embed = message_object_.GetEmbed()
        """
        return self.embed_

    def GetFile(self) -> Optional[File]:
        """
        Get the file object

        Returns:
        - The file object

        NOTE
        - If the file object is not set, it will return None
        - None is intended so that discord will treat it as no file to be sent

        Example:
        >>> message_object_ = MessageObject()
        >>> message_object_.SetFile(fp="image.jpg", filename="image.jpg", description="This is an image")
        >>> file_object : File = message_object_.GetFile()
        """
        return self.file_