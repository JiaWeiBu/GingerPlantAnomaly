"""
This file contains the logic for the discord bot,
This will be the main entry point for the discord bot,
Bot Method or characteristic will be written in channel.py
"""

from os import getenv
from dotenv import load_dotenv
from discord import Client, Message, Intents
from channel import MESSAGE_UNIT, RegisterChannelConfig, RegisterChannel, SendMessage

load_dotenv()
TOKEN : str = str(getenv('TOKEN_BOT_GITHUB'))
INTENTS : Intents = Intents.default()
INTENTS.message_content = True
CLIENT : Client = Client(intents=INTENTS)

def SystemInit() -> None:
    """
    Function to initialize the system
    """
    RegisterChannelConfig()

# Evnet Handlers
@CLIENT.event
async def on_ready() -> None:
    print(f'{CLIENT.user} has connected to Discord!')
    await RegisterChannel()


@CLIENT.event
async def on_message(message: Message) -> None:
    if message.author == CLIENT.user:
        return

    if not message.content.startswith(MESSAGE_UNIT.keyword_):
        return
    
    await SendMessage(message)

def run() -> None:
    SystemInit()
    CLIENT.run(token=TOKEN)

if __name__ == "__main__":
    run()