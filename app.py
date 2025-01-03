from os import getenv
from dotenv import load_dotenv
from random import randint
from discord import Client, Message, Intents
from classes.discord_lib import MessageObject
from classes.message_lib import MessageUnit, INIT_PHRASE, WebhookSend

load_dotenv()
TOKEN : str = str(getenv('TOKEN_BOT_GITHUB'))
INTENTS : Intents = Intents.default()
INTENTS.message_content = True
CLIENT : Client = Client(intents=INTENTS)
MESSAGE_UNIT = MessageUnit()

async def SendMessage(message: Message) -> None:
    response : MessageObject = MESSAGE_UNIT.GetResponse(message)

    if not response.EmptyMessage():
        await message.channel.send(response.message_, embed=response.embed_, file=response.file_) # type: ignore

# Evnet Handlers
@CLIENT.event
async def on_ready() -> None:
    print(f'{CLIENT.user} has connected to Discord!')
    print(f"Setting up the channels")
    for channel in MESSAGE_UNIT.ChannelEnum:
        MESSAGE_UNIT.SetChannelWebhookUrl(channel=channel, webhook_url=str(getenv(MESSAGE_UNIT.channel_object_dict_[channel].webhook_env_)))
        MESSAGE_UNIT.SetChannelPass(channel=channel, pass_=randint(100000, 999999))
        await WebhookSend(webhook_url=MESSAGE_UNIT.channel_object_dict_[channel].webhook_url_, content=f"{INIT_PHRASE} {MESSAGE_UNIT.channel_object_dict_[channel].pass_}")
    print(f"Init Configurations are done")


@CLIENT.event
async def on_message(message: Message) -> None:
    if message.author == CLIENT.user:
        return
    
    await SendMessage(message)

def run() -> None:
    CLIENT.run(token=TOKEN)

if __name__ == "__main__":
    run()

