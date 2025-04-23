# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from os import getenv
from dotenv import load_dotenv
from asyncio import new_event_loop, set_event_loop
from threading import Thread
from sys import stderr
from flask import request, Response
from PIL import Image
from io import BytesIO
from base64 import b64encode

from anomalib_train import RunModelAsync
from classes.flask_lib import Get, APP, Post
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
    """
      ModelTypeFlag.ai_vad_ : False,
        ModelTypeFlag.cfa_ : True,
        ModelTypeFlag.cflow_ : True,
        ModelTypeFlag.csflow_ : True,
        ModelTypeFlag.draem_ : True,
        ModelTypeFlag.dfkde_ : True,
        ModelTypeFlag.dfm_ : True,
        ModelTypeFlag.dsr_ : True,
        ModelTypeFlag.efficient_ad_ : True,
        ModelTypeFlag.fastflow_ : True,
        ModelTypeFlag.fre_ : True,
        ModelTypeFlag.ganomaly_ : True,
        ModelTypeFlag.padim_ : True,
        ModelTypeFlag.patchcore_ : True,
        ModelTypeFlag.reverse_distillation_ : True,
        ModelTypeFlag.rkde_ : True,
        ModelTypeFlag.stfpm_ : True,
        ModelTyp~eFlag.uflow_ : True,
        ModelTypeFlag.vlm_ad_ : False,
        ModelTypeFlag.win_clip_ : True


         I want cflow, fastflow, patchcore, reverse_distillation, stfpm
    """
    
    model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.cflow_ | AnomalyModelUnit.ModelTypeFlag.fastflow_ | AnomalyModelUnit.ModelTypeFlag.patchcore_ | AnomalyModelUnit.ModelTypeFlag.reverse_distillation_ | AnomalyModelUnit.ModelTypeFlag.stfpm_
    # continue from reverse_distillation_ to stfpm_
    #model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.reverse_distillation_ | AnomalyModelUnit.ModelTypeFlag.stfpm_

    # inverse for above
    #model_type_flag : AnomalyModelUnit.ModelTypeFlag = AnomalyModelUnit.ModelTypeFlag.cflow_ | AnomalyModelUnit.ModelTypeFlag.fastflow_ | AnomalyModelUnit.ModelTypeFlag.patchcore_

    logger_instance : LoggerWebhook = LoggerWebhook(webhook_link=link, clone_cmd="~clone", close_cmd="~close")

    await RunModelAsync(model_type_flag=model_type_flag, logger_instance_async=logger_instance, name="T5_Full_Individual_Filtered_Week_Unseen_Week3_Save_SimMutiAnomaly")

   
@Get 
async def Train() -> str:
    # cringe line here
    Thread(target=RunLoopSync, daemon=True).start()

    return "Training"

@Post
async def Predict() -> Response:
    """
    Handle the POST request to predict anomalies from multiple images and return multiple messages and images as a response.
    """
    if 'images' not in request.files:
        return {"error": "No image files provided"}, 400

    # Retrieve the image files from the request
    image_files = request.files.getlist('images')

    response_messages = []
    response_images = []

    try:
        for image_file in image_files:
            # Open the image using PIL
            image = Image.open(image_file.stream)

            # Perform prediction logic here
            # For demonstration, we'll just convert the image to grayscale
            grayscale_image = image.convert("L")

            # Save the processed image to an in-memory buffer
            image_buffer = BytesIO()
            grayscale_image.save(image_buffer, format="PNG")
            image_buffer.seek(0)

            # Encode the image as Base64
            image_base64 = b64encode(image_buffer.getvalue()).decode('utf-8')

            # Add a success message and the processed image to the response
            response_messages.append(f"Prediction successful for {image_file.filename}")
            response_images.append(image_base64)

        # Return text and images in JSON
        return {
            "messages": response_messages,
            "images": response_images
        }, 200

    except Exception as e:
        return {"error": f"Error processing images: {str(e)}"}, 500

def flask_run():
    APP.run()
    
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
