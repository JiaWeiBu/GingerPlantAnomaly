# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from os import getenv, makedirs
from os.path import join, exists
from shutil import rmtree
from uuid import uuid4
from dotenv import load_dotenv
from asyncio import new_event_loop, set_event_loop
from threading import Thread
from sys import stderr
from flask import request, Response
from io import BytesIO
from base64 import b64encode
from json import dumps  # Add this import for JSON serialization


from anomalib_train import RunModelAsync
from anomalib_test import AnomalibTest, ModelPathUnit
from classes.flask_lib import Get, APP, Post
from classes.discord_lib import MessageObject
from classes.message_lib import WebhookSend
from classes.anomalib_lib import AnomalyModelUnit
from classes.log_lib import LoggerWebhook



# load the environment variables
load_dotenv()
link : str = str(getenv('CHANNEL_WEBHOOK_CLONE'))
anomalib_test : AnomalibTest = AnomalibTest()
model_path_unit : ModelPathUnit = ModelPathUnit()

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
async def PredictSetup() -> Response:
    """
    Handle the POST request to set up the prediction environment.
    """
    # Extract 'week' and 'name' from the request form
    week = request.form.get('week')
    name = request.form.get('name')

    if not week or not name:
        return Response("Both 'week' and 'name' are required.", status=400)

    try:
        week_int = int(week)  # Convert week to integer
    except ValueError:
        return Response("'week' must be an integer.", status=400)

    # Validate the model path using ModelPathUnit.IsValid()
    valid_result = model_path_unit.IsValid(week=week_int, types=name)
    if not valid_result:
        return Response("Invalid model path for the provided 'week' and 'name'.", status=400)

    model_type_enum, model_week_enum = valid_result

    # Run the setup for AnomalibTest
    anomalib_test.Setup(model_path=model_path_unit.ModelPath(types=model_type_enum, week=model_week_enum))

    return Response("Setup successful", status=200)

@Post
async def Predict() -> Response:
    """
    Handle the POST request to predict anomalies from multiple images and return multiple messages and images as a response.
    """
    if 'images' not in request.files:
        return Response(
            dumps({
                "messages": ["No image files provided."],
                "images": []
            }),
            status=400,
            mimetype="application/json"
        )

    # Retrieve the image files from the request
    image_files = request.files.getlist('images')

    # Create a temporary directory with a random name
    temp_dir = join("testtest", str(uuid4()))
    makedirs(temp_dir, exist_ok=True)

    response_messages = []
    response_images = []

    try:
        # Save each image to the temporary directory
        for image_file in image_files:
            assert image_file.filename is not None, "Image filename is None"
            image_path = join(temp_dir, image_file.filename)
            image_file.save(image_path)

        # Evaluate the images using anomalib_test
        results = anomalib_test.Evaluate(image_path=temp_dir)

        # Process the results
        for result_image, result_string in results:
            # Save the result image as PNG (supports RGBA)
            image_buffer = BytesIO()
            result_image.save(image_buffer, format="PNG")
            image_buffer.seek(0)
            image_base64 = b64encode(image_buffer.getvalue()).decode('utf-8')

            # Add the result string and image to the response
            response_messages.append(result_string)
            response_images.append(image_base64)

        # Clean up the temporary directory
        rmtree(temp_dir, ignore_errors=True)

        # Return text and images in JSON
        return Response(
            dumps({
                "messages": response_messages,
                "images": response_images
            }),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        # Clean up the temporary directory in case of an error
        rmtree(temp_dir, ignore_errors=True)
        return Response(
            dumps({
                "messages": [f"Error processing images: {str(e)}"],
                "images": []
            }),
            status=500,
            mimetype="application/json"
        )
    
    finally:
        # Clean up the temporary directory if it exists
        if exists(temp_dir):
            rmtree(temp_dir, ignore_errors=True)

def flask_run():
    APP.run()
    
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
