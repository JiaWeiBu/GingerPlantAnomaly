# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from os import getenv
from dotenv import load_dotenv
from asyncio import create_task, sleep, new_event_loop, set_event_loop
from threading import Thread
from sys import stderr

from anomalib_train import RunModelAsync
from classes.flask_lib import Get, APP
from classes.discord_lib import MessageObject
from classes.message_lib import WebhookSend
from classes.anomalib_lib import AnomalyModelUnit
from classes.log_lib import LoggerWebhook



# load the environment variables
load_dotenv()
link : str = str(getenv('CHANNEL_WEBHOOK_CLONE'))

# API Function from Server
@Get
async def Test() -> str:
    message_object = MessageObject()
    message_object.SetFile("./datasets/re_plant/train/60/00001.jpg", filename="test.jpg", description="Test Description")
    message_object.SetMessage("~clone Test Clone")
    message_object.CreateEmbed(title="Test Image Clone", description="Test Image Description Clone")
    message_object.EmbedSetImage(url="attachment://test.jpg")
    await WebhookSend(webhook_url=link, message_object=message_object)
    return "Success"

@Get
async def Index() -> str:
    message_object = MessageObject()
    message_object.SetMessage("Hello World")
    print("Hello World", file=stderr)
    await WebhookSend(webhook_url=link, message_object=message_object)
    return "Hello World"

def RunLoopSync() -> None:
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(RunTrainAsync())

async def RunTrainAsync() -> None:
    model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.padim_ | AnomalyModelUnit.ModelTypeFlag.dfkde_  | AnomalyModelUnit.ModelTypeFlag.stfpm_ | AnomalyModelUnit.ModelTypeFlag.draem_ | AnomalyModelUnit.ModelTypeFlag.reverse_distillation_ | AnomalyModelUnit.ModelTypeFlag.ganomaly_

    logger_instance : LoggerWebhook = LoggerWebhook(webhook_link=link, clone_cmd="~clone", close_cmd="~close")

    await RunModelAsync(model_type_flag=model_type_flag, logger_instance_async=logger_instance, name="T5_Full_Individual_Filtered_Week_Unseen_Week3_Save_SimMutiAnomaly")

   
@Get 
async def Train() -> str:
    # cringe line here
    Thread(target=RunLoopSync, daemon=True).start()

    return "Training"

def flask_run():
    APP.run()
    
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
    