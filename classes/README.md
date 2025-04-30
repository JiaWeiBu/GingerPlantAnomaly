# Class Documentation

[Back to Main README](../README.md)

## Table of Contents
- [Overview](#overview)
- [anomalib_lib.py](#anomalib_libpy)
- [channel_enum.py](#channel_enumpy)
- [dataset_lib.py](#dataset_libpy)
- [discord_lib.py](#discord_libpy)
- [flask_lib.py](#flask_libpy)
- [general_lib.py](#general_libpy)
- [log_lib.py](#log_libpy)
- [message_lib.py](#message_libpy)
- [progress_lib.py](#progress_libpy)
- [pycaret_lib.py](#pycaret_libpy)
- [util_lib.py](#util_libpy)

## Overview
This folder contains the core classes and utility functions used in the GingerPlantAnomaly project. Each file serves a specific purpose, as described below.

## Documentation Links
- [PyCaret Documentation](https://pycaret.readthedocs.io/en/stable/api/anomaly.html#pycaret.anomaly.models)
- [Anomalib Documentation (v1.2.0)](https://github.com/openvinotoolkit/anomalib/tree/v1.2.0)  
  **Note**: This project uses version `1.2.0` of Anomalib. The latest version (`2.0.0`) is not compatible with the current implementation.
- [Discord.py Documentation](https://discordpy.readthedocs.io/en/stable/)

---

### `anomalib_lib.py`
**Purpose**: Implements Anomalib-based anomaly detection models.

#### Classes:
1. **`AnomalyModelUnit`**:
   - **Purpose**: Provides a framework for training, evaluating, and predicting using Anomalib models.
   - **Enums**:
     - **`ModelTypeFlag`**:
       - **Purpose**: Enum for different types of anomaly detection models.
       - **Attributes**:
         - Examples: `ai_vad_`, `cfa_`, `cflow_`, `fastflow_`, `patchcore_`, etc.
       - **Example**:
         ```python
         model_type = AnomalyModelUnit.ModelTypeFlag.cflow_
         ```
     - **`AnomalibLoggerTypeEnum`**:
       - **Purpose**: Enum for different types of loggers.
       - **Attributes**:
         - Examples: `comet_`, `mlflow_`, `tensorboard_`, `wandb_`.
       - **Example**:
         ```python
         logger_type = AnomalyModelUnit.AnomalibLoggerTypeEnum.tensorboard_
         ```
     - **`AnomalibTaskTypeEnum`**:
       - **Purpose**: Enum for different types of tasks.
       - **Attributes**:
         - Examples: `classification_`, `detection_`, `segmentation_`.
       - **Example**:
         ```python
         task_type = AnomalyModelUnit.AnomalibTaskTypeEnum.classification_
         ```
     - **`AnomalibLearningTypeEnum`**:
       - **Purpose**: Enum for different types of learning.
       - **Attributes**:
         - Examples: `one_class_`, `zero_shot_`, `few_shot_`.
       - **Example**:
         ```python
         learning_type = AnomalyModelUnit.AnomalibLearningTypeEnum.one_class_
         ```
   - **Attributes**:
     - `model_`: Internal Anomalib model instance.
     - `engine_`: Internal Anomalib engine instance.
     - `model_type_`: Selected model type.
     - `image_metrics_`: List of image metrics for evaluation.
     - `task_`: Task type for the model.
   - **Methods**:
     - **`Setter`**:
       - **Purpose**: Sets the model parameters.
       - **Args**:
         - `model_type (ModelTypeFlag)`: Model type.
         - `image_metrics (list[str])`: Image metrics.
         - `task (AnomalibTaskTypeEnum)`: Task type.
       - **Example**:
         ```python
         model.Setter(model_type=AnomalyModelUnit.ModelTypeFlag.fastflow_)
         ```
     - **`Train`**:
       - **Purpose**: Trains the model using a dataset.
       - **Args**:
         - `datamodule (Folder)`: Dataset for training.
       - **Example**:
         ```python
         model.Train(datamodule=datamodule)
         ```
     - **`Evaluate`**:
       - **Purpose**: Evaluates the trained model.
       - **Args**:
         - `datamodule (Folder)`: Dataset for evaluation.
       - **Example**:
         ```python
         results = model.Evaluate(datamodule=datamodule)
         ```
     - **`Predict`**:
       - **Purpose**: Predicts anomalies in a dataset.
       - **Args**:
         - `data (Folder)`: Dataset for prediction.
       - **Returns**: Predicted anomalies.
       - **Example**:
         ```python
         predictions = model.Predict(data=test_data)
         ```
     - **`Save`**:
       - **Purpose**: Saves the trained model.
       - **Args**:
         - `path (str)`: Path to save the model.
       - **Example**:
         ```python
         model.Save(path="model_path")
         ```
     - **`ModelValid`**:
       - **Purpose**: Checks if the selected model is valid.
       - **Args**:
         - `model_type (ModelTypeFlag)`: Model type.
       - **Returns**: `True` if valid, `False` otherwise.
       - **Example**:
         ```python
         is_valid = model.ModelValid(model_type=AnomalyModelUnit.ModelTypeFlag.cflow_)
         ```

#### Notes:
- **Validation**: The `ModelValid` method ensures that only supported models are used.
- **Usage**: This class provides a modular approach to anomaly detection using Anomalib.

---

### `channel_enum.py`
**Purpose**: Defines enums for channel IDs used in the project.

#### Enums:
1. **`ChannelEnum`**:
   - **Purpose**: Enum class for managing channel IDs used in the Discord bot.
   - **Attributes**:
     - `log_`: Log channel ID.
     - `predict_`: Prediction channel ID, where users send images and messages to be answered.
     - `debug_`: Debug channel ID for training or debugging purposes.
     - `clone_`: Clone channel ID for duplicating threads or messages.
   - **Example**:
     ```python
     from classes.channel_enum import ChannelEnum
     
     channel = ChannelEnum.log_
     print(channel.name)  # Output: "log_"
     ```

#### Notes:
- **Integration**: This enum is used in conjunction with the `MessageUnit` class in `message_lib.py` to manage Discord bot channels.
- **Customization**: Additional channels can be added to this enum as needed for new functionalities.

---

### `dataset_lib.py`
**Purpose**: Handles dataset loading, preprocessing, and management.

#### Classes:
1. **`ImageUnit`**:
   - **Purpose**: Provides utilities for image processing, including loading, saving, resizing, color conversion, and cropping.
   - **Enums**:
     - **`ColorModeEnum`**:
       - **Purpose**: Enum for different color modes for image processing.
       - **Attributes**:
         - `rgb_`: RGB color mode.
         - `grayscale_`: Grayscale color mode.
       - **Example**:
         ```python
         color_mode = ImageUnit.ColorModeEnum.rgb_
         ```
     - **`ColorConversionEnum`**:
       - **Purpose**: Enum for different color conversion methods for image processing.
       - **Attributes**:
         - `rgb2gray_`: RGB to Grayscale conversion.
         - `gray2rgb_`: Grayscale to RGB conversion.
       - **Example**:
         ```python
         conversion = ImageUnit.ColorConversionEnum.rgb2gray_
         ```
     - **`ImageInterpolationEnum`**:
       - **Purpose**: Enum for different interpolation methods for image resizing.
       - **Attributes**:
         - `nearest_`, `linear_`, `cubic_`, `lanczos4_`: Interpolation methods.
       - **Example**:
         ```python
         interpolation = ImageUnit.ImageInterpolationEnum.linear_
         ```
   - **Methods**:
     - **`LoadImage`**:
       - **Purpose**: Loads an image from a file.
       - **Args**:
         - `path (str)`: Path to the image file.
         - `color_mode (ColorModeEnum)`: Color mode of the image.
       - **Example**:
         ```python
         image = image_unit.LoadImage("path/to/image.jpg", ImageUnit.ColorModeEnum.rgb_)
         ```
     - **`SaveImage`**:
       - **Purpose**: Saves an image to a file.
       - **Args**:
         - `path (str)`: Path to save the image.
         - `image (ndarray)`: Image data.
       - **Example**:
         ```python
         image_unit.SaveImage("path/to/save/image.jpg", image)
         ```
     - **`ResizeImage`**:
       - **Purpose**: Resizes an image.
       - **Args**:
         - `image (ndarray)`: Image data.
         - `size (Size)`: Size to resize the image.
         - `interpolation (ImageInterpolationEnum)`: Interpolation method.
       - **Example**:
         ```python
         resized_image = image_unit.ResizeImage(image, Size(100, 100), ImageUnit.ImageInterpolationEnum.linear_)
         ```
     - **`ConvertColor`**:
       - **Purpose**: Converts the color of an image.
       - **Args**:
         - `image (ndarray)`: Image data.
         - `conversion (ColorConversionEnum)`: Color conversion method.
       - **Example**:
         ```python
         converted_image = image_unit.ConvertColor(image, ImageUnit.ColorConversionEnum.rgb2gray_)
         ```
     - **`CropImage`**:
       - **Purpose**: Crops an image.
       - **Args**:
         - `image (ndarray)`: Image data.
         - `rect (Rect)`: Rectangle to crop the image.
       - **Example**:
         ```python
         cropped_image = image_unit.CropImage(image, Rect(Point(0, 0), Size(100, 100)))
         ```
     - **`ShowImage`**:
       - **Purpose**: Displays an image.
       - **Args**:
         - `image (ndarray)`: Image data.
         - `name (str)`: Name of the window.
       - **Example**:
         ```python
         image_unit.ShowImage(image, "Image")
         ```

2. **`DatasetUnit`**:
   - **Purpose**: Manages dataset operations, including loading, resizing, and validating images.
   - **Enums**:
     - **`MVTecDatasetTypeEnum`**:
       - **Purpose**: Enum for different MVTec dataset types.
       - **Attributes**:
         - Examples: `bottle_`, `cable_`, `capsule_`, `carpet_`, `grid_`, etc.
       - **Example**:
         ```python
         dataset_type = DatasetUnit.MVTecDatasetTypeEnum.bottle_
         ```
     - **`MVTecDatasetTypeAnomalyEnum`**:
       - **Purpose**: Enum for different MVTec dataset anomaly types.
       - **Attributes**:
         - Examples: `broken_large_`, `broken_small_`, `contamination_`, `bent_wire_`, `crack_`, etc.
       - **Example**:
         ```python
         anomaly_type = DatasetUnit.MVTecDatasetTypeAnomalyEnum.broken_large_
         ```
   - **Attributes**:
     - `MVTecDataset`: Dictionary mapping MVTec dataset types to their respective anomaly types.
     - `image_unit_`: Instance of `ImageUnit` for image processing.
     - `images_`: List of loaded images.
     - `images_name_`: List of image names.
   - **Methods**:
     - **`ClearDataset`**:
       - **Purpose**: Clears the dataset.
       - **Example**:
         ```python
         dataset_unit.ClearDataset()
         ```
     - **`DirImages`**:
       - **Purpose**: Reads a directory and retrieves all image files.
       - **Args**:
         - `path (str)`: Path to the directory.
       - **Example**:
         ```python
         image_paths = dataset_unit.DirImages("path/to/images")
         ```
     - **`LoadImagesName`**:
       - **Purpose**: Loads image names from a specified directory.
       - **Args**:
         - `paths (str)`: Path to the directory.
       - **Example**:
         ```python
         dataset_unit.LoadImagesName("path/to/images")
         ```
     - **`LoadImages`**:
       - **Purpose**: Loads images from a directory and stores them in the dataset.
       - **Args**:
         - `paths (str)`: Path to the directory.
         - `color_mode (ImageUnit.ColorModeEnum)`: Color mode of the images.
       - **Example**:
         ```python
         dataset_unit.LoadImages("path/to/images", ImageUnit.ColorModeEnum.rgb_)
         ```
     - **`LoadImagesResize`**:
       - **Purpose**: Loads and resizes images from a directory.
       - **Args**:
         - `paths (str)`: Path to the directory.
         - `color_mode (ImageUnit.ColorModeEnum)`: Color mode of the images.
         - `size (Size)`: Size to resize the images.
       - **Example**:
         ```python
         dataset_unit.LoadImagesResize("path/to/images", ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
         ```
     - **`LoadImagesResize2D`**:
       - **Purpose**: Loads and resizes images into 2D arrays.
       - **Args**:
         - `paths (str)`: Path to the directory.
         - `color_mode (ImageUnit.ColorModeEnum)`: Color mode of the images.
         - `size (Size)`: Size to resize the images.
       - **Example**:
         ```python
         dataset_unit.LoadImagesResize2D("path/to/images", ImageUnit.ColorModeEnum.rgb_, Size(100, 100))
         ```
     - **`AnomalibLoadFolder`**:
       - **Purpose**: Loads a dataset for Anomalib.
       - **Args**:
         - `root_path (str)`: Path to the root directory.
         - `normal_path (list[str])`: List of paths to normal images.
         - `abnormal_path (list[str])`: List of paths to abnormal images.
         - `normal_split_ratio (float)`: Ratio of normal images for testing.
         - `test_split_ratio (float)`: Ratio of test images.
         - `datalib_name (str)`: Name of the dataset.
         - `size (Size)`: Size to resize the images.
         - `task (TaskType)`: Task type of the dataset.
       - **Example**:
         ```python
         dataset_unit.AnomalibLoadFolder(
             root_path="datasets/bottle",
             normal_path=["train/good"],
             abnormal_path=["test/broken_large", "test/broken_small"],
             normal_split_ratio=0.2,
             test_split_ratio=0.2,
             datalib_name="bottle",
             size=Size(64, 64),
             task=TaskType.CLASSIFICATION
         )
         ```
     - **`AnomalibDatasetValidation`**:
       - **Purpose**: Validates the dataset.
       - **Example**:
         ```python
         dataset_unit.AnomalibDatasetValidation()
         ```

#### Notes:
- **Validation**: The `AnomalibDatasetValidation` method ensures the dataset is properly initialized and ready for use.
- **Usage**: These classes and methods are designed to streamline dataset operations for anomaly detection tasks.

---

### `discord_lib.py`
**Purpose**: Manages Discord bot messages and interactions.

#### Classes:
1. **`MessageObject`**:
   - **Purpose**: Represents a Discord message object, including embeds, text, and file attachments.
   - **Enums**:
     - **`EmbedColourEnum`**:
       - **Purpose**: Enum for different colors used in Discord embeds.
       - **Attributes**:
         - `blue_`, `green_`, `red_`, `random_`, `dark_blue_`, `gold_`, `purple_`, `teal_`, etc.
       - **Example**:
         ```python
         color = MessageObject.EmbedColourEnum.blue_
         ```
   - **Attributes**:
     - `embed_`: Embed object for Discord messages.
     - `message_`: Text message content.
     - `file_`: File object for attachments.
   - **Methods**:
     - **`SetMessage`**:
       - **Purpose**: Sets the message content.
       - **Args**:
         - `message (str)`: The message content.
       - **Example**:
         ```python
         message_object.SetMessage("Hello World")
         ```
     - **`CreateEmbed`**:
       - **Purpose**: Creates an embed object.
       - **Args**:
         - `title (str)`: Title of the embed.
         - `description (str)`: Description of the embed.
         - `colour (Colour)`: Color of the embed.
       - **Example**:
         ```python
         message_object.CreateEmbed(title="Title", description="Description")
         ```
     - **`EmbedSetFooter`**:
       - **Purpose**: Sets the footer for the embed.
       - **Args**:
         - `text (str)`: Footer text.
         - `icon_url (str)`: URL for the footer icon.
       - **Example**:
         ```python
         message_object.EmbedSetFooter(text="Footer Text", icon_url="https://example.com/icon.png")
         ```
     - **`EmbedAddField`**:
       - **Purpose**: Adds a field to the embed.
       - **Args**:
         - `name (str)`: Field name.
         - `value (str)`: Field value.
         - `inline (bool)`: Whether the field is inline.
       - **Example**:
         ```python
         message_object.EmbedAddField(name="Field Name", value="Field Value")
         ```
     - **`EmbedSetImage`**:
       - **Purpose**: Sets an image for the embed.
       - **Args**:
         - `url (str)`: URL of the image.
       - **Example**:
         ```python
         message_object.EmbedSetImage(url="https://example.com/image.png")
         ```
     - **`EmbedSetThumbnail`**:
       - **Purpose**: Sets a thumbnail for the embed.
       - **Args**:
         - `url (str)`: URL of the thumbnail.
       - **Example**:
         ```python
         message_object.EmbedSetThumbnail(url="https://example.com/thumbnail.png")
         ```
     - **`SetFile`**:
       - **Purpose**: Attaches a file to the message.
       - **Args**:
         - `fp (str | bytes)`: File path or binary data.
         - `filename (str)`: Name of the file.
         - `description (str)`: Description of the file.
       - **Example**:
         ```python
         message_object.SetFile(fp="image.jpg", filename="image.jpg", description="An image")
         ```
     - **`GetMessage`**:
       - **Purpose**: Retrieves the message content.
       - **Returns**: The message content as a string.
       - **Example**:
         ```python
         message = message_object.GetMessage()
         ```
     - **`GetEmbed`**:
       - **Purpose**: Retrieves the embed object.
       - **Returns**: The embed object.
       - **Example**:
         ```python
         embed = message_object.GetEmbed()
         ```
     - **`GetFile`**:
       - **Purpose**: Retrieves the file object.
       - **Returns**: The file object.
       - **Example**:
         ```python
         file = message_object.GetFile()
         ```

#### Notes:
- **Discord Embed Limit**: Discord allows a maximum of **10 embeds** per message. The current implementation does not handle this limitation. Future upgrades may require splitting messages or managing multiple embeds.
- **File Attachments**: The `SetFile` method supports attaching images, videos, and other files to Discord messages.

---

### `flask_lib.py`
**Purpose**: Implements a Flask-based API for managing routes.

#### Enums:
- **`CallbackFunctionRoute`**:
  - **Purpose**: Enum class for registering routes to callback functions.
  - **Attributes**:
    - `ApiService`: Route for the API service (`/api`).
    - `Index`: Route for the index page (`/`).
    - `Test`: Route for testing purposes (`/test`).
    - `Train`: Route for training models (`/train`).
    - `Predict`: Route for making predictions (`/predict`).
    - `PredictSetup`: Route for setting up prediction configurations (`/predict_setup`).
  - **Example**:
    ```python
    CALLBACK_FUNCTION_ROUTE["ApiService"]  # Output: '/api'
    ```

#### Decorators:
- **`Callback`**:
  - **Purpose**: Generic decorator for registering a route to a callback function.
  - **Usage**:
    ```python
    @Callback
    def ApiService():
        return jsonify({"message": "API Service"})
    ```
- **`Get`**:
  - **Purpose**: Registers a GET route.
  - **Usage**:
    ```python
    @Get
    def Index():
        return "Hello World"
    ```
- **`Post`**:
  - **Purpose**: Registers a POST route.
  - **Usage**:
    ```python
    @Post
    def Train():
        return "Training started"
    ```
- **`GetPost`**:
  - **Purpose**: Registers both GET and POST routes.
  - **Usage**:
    ```python
    @GetPost
    def Predict():
        return "Prediction endpoint"
    ```

#### Methods:
- **`ApiService`**:
  - **Purpose**: Example function registered with the `Get` decorator.
  - **Returns**: JSON response with the registered routes.
  - **Example**:
    ```bash
    curl http://localhost:5000/api
    ```
- **`Index`**:
  - **Purpose**: Example function registered with the `Get` decorator.
  - **Returns**: A simple "Hello World" string.
  - **Example**:
    ```bash
    curl http://localhost:5000/
    ```
- **`Train`**:
  - **Purpose**: Example function registered with the `Post` decorator.
  - **Returns**: A string indicating that training has started.
  - **Example**:
    ```bash
    curl -X POST http://localhost:5000/train
    ```
- **`Predict`**:
  - **Purpose**: Example function registered with the `GetPost` decorator.
  - **Returns**: A string indicating the prediction endpoint.
  - **Example**:
    ```bash
    curl http://localhost:5000/predict
    curl -X POST http://localhost:5000/predict
    ```

#### Flask App:
- **`APP`**:
  - **Purpose**: Flask application instance.
  - **Details**: Provides an API for interacting with the project.

---

### `general_lib.py`
**Purpose**: Provides utility classes for managing paths, image information, and training/testing configurations.

#### Functions:
- **`Singleton`**:
  - **Purpose**: Ensures a class has only one unique instance.
  - **Example**:
    ```python
    @Singleton
    class MyClass:
        pass
    ```

#### Classes:
1. **`PredictPathObject`**:
   - **Attributes**:
     - `root_`: Root path for prediction.
     - `model_`: Path to the model.
     - `test_good_`: Path to good test data.
     - `test_defective_`: Path to defective test data.
   - **Purpose**: Manages paths for prediction tasks.
   - **Example**:
     ```python
     path = PredictPathObject("root", "model.pt", "test_good", "test_defective")
     print(path.test_good_)  # Output: "test_good"
     ```

2. **`ImageInfoObject`**:
   - **Attributes**:
     - `size_`: Size of the image.
     - `colour_mode_`: Colour mode of the image.
     - `name_`: Name of the image.
   - **Purpose**: Stores metadata about an image.
   - **Example**:
     ```python
     img_info = ImageInfoObject(Size(100, 100), ImageUnit.ColorModeEnum.rgb_, "image_name")
     print(img_info.size_)  # Output: Size(100, 100)
     ```

3. **`TrainPathObject`**:
   - **Attributes**:
     - `root_`: Root path for training.
     - `train_`: List of paths to training data.
     - `test_good_`: List of paths to good test data.
     - `test_defective_`: List of paths to defective test data.
     - `model_save_`: Path to save the model.
   - **Purpose**: Manages paths for training tasks.
   - **Example**:
     ```python
     path = TrainPathObject("root", ["train"], ["test_good"], ["test_defective"], "model_save")
     print(path.train_)  # Output: ["train"]
     ```

4. **`TrainObject`**:
   - **Attributes**:
     - `path_`: TrainPathObject instance for training paths.
     - `image_info_`: ImageInfoObject instance for image metadata.
   - **Purpose**: Combines training paths and image metadata.
   - **Example**:
     ```python
     train = TrainObject(
         TrainPathObject("root", ["train"], ["test_good"], ["test_defective"], "model_save"),
         ImageInfoObject(Size(100, 100), ImageUnit.ColorModeEnum.rgb_, "image_name")
     )
     print(train.path_.train_)  # Output: ["train"]
     ```

5. **`TestPathObject`**:
   - **Attributes**:
     - `root_`: Root path for testing.
     - `test_good_`: List of paths to good test data.
     - `test_defective_`: List of paths to defective test data.
     - `test_mask_`: List of paths to test masks.
   - **Purpose**: Manages paths for testing tasks.
   - **Example**:
     ```python
     path = TestPathObject("root", ["test_good"], ["test_defective"], ["test_mask"])
     print(path.test_good_)  # Output: ["test_good"]
     ```

6. **`TestObject`**:
   - **Attributes**:
     - `path_`: TestPathObject instance for testing paths.
     - `image_info_`: ImageInfoObject instance for image metadata.
   - **Purpose**: Combines testing paths and image metadata.
   - **Example**:
     ```python
     test = TestObject(
         TestPathObject("root", ["test_good"], ["test_defective"], ["test_mask"]),
         ImageInfoObject(Size(100, 100), ImageUnit.ColorModeEnum.rgb_, "test")
     )
     print(test.path_.test_good_)  # Output: ["test_good"]
     ```

---

### `log_lib.py`
**Purpose**: Provides logging utilities for the project, including file-based logging, Discord-based logging, and webhook-based logging.

#### Classes:
1. **`LoggerTemplate`**:
   - **Purpose**: A base template for logging.
   - **Methods**:
     - **`Open`**: Opens the logger.
     - **`Output`**: Outputs text to the logger.
     - **`Close`**: Closes the logger.
   - **Example**:
     ```python
     logger = LoggerTemplate()
     logger.Output(text="Hello World")
     ```

2. **`AsyncLoggerTemplate`**:
   - **Purpose**: A base template for asynchronous logging.
   - **Methods**:
     - **`Open`**: Opens the logger asynchronously.
     - **`Output`**: Outputs text to the logger asynchronously.
     - **`Close`**: Closes the logger asynchronously.
   - **Example**:
     ```python
     logger = AsyncLoggerTemplate()
     await logger.Output(text="Hello World")
     ```

3. **`LoggerFile`**:
   - **Purpose**: A file-based logger for writing logs to a file.
   - **Attributes**:
     - `file_`: The file object.
     - `open_`: Boolean indicating if the file is open.
   - **Methods**:
     - **`Open`**: Opens the file for writing.
     - **`Output`**: Writes text to the file.
     - **`Close`**: Closes the file.
   - **Example**:
     ```python
     logger = LoggerFile()
     logger.Open(file_name="log.txt", modes="w")
     logger.Output(text="Hello World")
     logger.Close()
     ```

4. **`LoggerDiscord`**:
   - **Purpose**: A Discord-based logger for sending logs to a Discord thread.
   - **Attributes**:
     - `thread_`: The Discord thread object.
   - **Methods**:
     - **`Setup`**: Sets up the logger by sending a webhook.
     - **`Open`**: Opens a thread for logging.
     - **`Output`**: Sends a message to the thread.
     - **`Close`**: Closes the thread.
   - **Example**:
     ```python
     logger = LoggerDiscord()
     await logger.Setup(webhook_link="https://discord.com/api/webhooks/...")

     await logger.Open(message=message, name="Log Thread", duration=1440)
     await logger.Output(message_object=message_object)
     await logger.Close()
     ```

5. **`LoggerWebhook`**:
   - **Purpose**: A webhook-based logger for sending logs to a Discord webhook.
   - **Attributes**:
     - `webhook_link_`: The Discord webhook link.
     - `message_object_`: The message object.
     - `clone_cmd_`: The clone command.
     - `close_cmd_`: The close command.
   - **Methods**:
     - **`Open`**: Opens the webhook logger.
     - **`Output`**: Sends a message to the webhook.
     - **`Close`**: Closes the webhook logger.
   - **Example**:
     ```python
     logger = LoggerWebhook(webhook_link="https://discord.com/api/webhooks/...", clone_cmd="~clone", close_cmd="~close")
     await logger.Output(message_object=message_object)
     await logger.Close()
     ```

#### Notes:
- **Singleton Decorator**: All logger classes use the `@Singleton` decorator to ensure only one instance of the logger exists.
- **Discord Integration**: The `LoggerDiscord` and `LoggerWebhook` classes integrate with Discord for logging, allowing logs to be sent to threads or webhooks.

---

### `message_lib.py`
**Purpose**: Manages Discord bot messages and interactions, including webhook communication and channel configuration.

#### Constants:
- **`INIT_PHRASE`**:
  - **Purpose**: The keyword used to initialize the system.
  - **Value**: `"ginie"`
  - **Example**:
    ```python
    INIT_PHRASE = "ginie"
    ```

#### Functions:
- **`WebhookSend`**:
  - **Purpose**: Sends a message to a Discord webhook URL.
  - **Args**:
    - `webhook_url (str)`: The URL of the webhook.
    - `message_object (MessageObject)`: The message object containing the content, embed, and file.
  - **Example**:
    ```python
    await WebhookSend("https://discord.com/api/webhooks/123456789", message_object=message_object)
    ```

#### Classes:
1. **`ChannelObject`**:
   - **Purpose**: Represents a Discord channel with its ID, webhook, and associated function.
   - **Attributes**:
     - `id_`: The channel ID.
     - `webhook_env_`: The webhook environment variable.
     - `webhook_url_`: The webhook URL.
     - `func_`: The function to run for the channel.
     - `pass_`: The password for the channel.
   - **Example**:
     ```python
     channel_object = ChannelObject(
         ids=123456789,
         webhook_env="CHANNEL_WEBHOOK_LOG",
         webhook_url="https://discord.com/api/webhooks/123456789",
         func=ResLog,
         password=123456
     )
     ```

2. **`MessageUnit`**:
   - **Purpose**: Manages Discord bot message routing and channel configuration.
   - **Attributes**:
     - `channel_id_dict_inv_`: Dictionary mapping channel IDs to their enums.
     - `channel_object_dict_`: Dictionary mapping channel enums to their `ChannelObject`.
     - `init_`: Boolean flag indicating if the system is initialized.
     - `num_channels_init_`: Number of channels to initialize.
     - `keyword_`: The keyword used to identify bot commands.
   - **Methods**:
     - **`__init__`**:
       - **Purpose**: Initializes the `MessageUnit` with a keyword.
       - **Args**:
         - `keyword (str)`: The keyword to identify bot commands.
       - **Example**:
         ```python
         message_unit = MessageUnit(keyword="ginie")
         ```
     - **`RegisterChannelObject`**:
       - **Purpose**: Registers a channel object.
       - **Args**:
         - `channel (Enum)`: The channel enum.
         - `channel_object (ChannelObject)`: The channel object to register.
       - **Example**:
         ```python
         message_unit.RegisterChannelObject(channel=ChannelEnum.log_, channel_object=channel_object)
         ```
     - **`SetChannelID`**:
       - **Purpose**: Sets the channel ID for a given channel.
       - **Args**:
         - `channel (Enum)`: The channel enum.
         - `channel_id (int)`: The channel ID.
       - **Example**:
         ```python
         message_unit.SetChannelID(channel=ChannelEnum.log_, channel_id=123456789)
         ```
     - **`SetChannelPass`**:
       - **Purpose**: Sets the password for a channel.
       - **Args**:
         - `channel (Enum)`: The channel enum.
         - `pass_ (int)`: The password.
       - **Example**:
         ```python
         message_unit.SetChannelPass(channel=ChannelEnum.log_, pass_=123456)
         ```
     - **`SetChannelWebhookUrl`**:
       - **Purpose**: Sets the webhook URL for a channel.
       - **Args**:
         - `channel (Enum)`: The channel enum.
         - `webhook_url (str)`: The webhook URL.
       - **Example**:
         ```python
         message_unit.SetChannelWebhookUrl(channel=ChannelEnum.log_, webhook_url="https://discord.com/api/webhooks/123456789")
         ```
     - **`ChannelDictInit`**:
       - **Purpose**: Initializes the channel ID dictionary.
       - **Example**:
         ```python
         message_unit.ChannelDictInit()
         ```
     - **`RunFunc`**:
       - **Purpose**: Executes the function associated with a channel.
       - **Args**:
         - `func (Callable)`: The function to execute.
         - `message (Message)`: The Discord message.
         - `message_object (MessageObject)`: The message object to store the response.
       - **Example**:
         ```python
         await message_unit.RunFunc(func=ResLog, message=discord_message, message_object=message_object)
         ```
     - **`GetResponse`**:
       - **Purpose**: Retrieves the response for a given message.
       - **Args**:
         - `message (Message)`: The Discord message.
       - **Returns**: A `MessageObject` containing the response.
       - **Example**:
         ```python
         response = await message_unit.GetResponse(discord_message)
         ```
     - **`InitRoutine`**:
       - **Purpose**: Initializes the system by setting channel IDs based on passwords.
       - **Args**:
         - `message (Message)`: The Discord message.
         - `message_object (MessageObject)`: The message object to store the response.
       - **Example**:
         ```python
         await message_unit.InitRoutine(discord_message, message_object)
         ```
     - **`DeleteMessage`**:
       - **Purpose**: Deletes a message after a delay.
       - **Args**:
         - `message (Message)`: The Discord message.
         - `delay_seconds (float)`: The delay in seconds before deletion.
       - **Example**:
         ```python
         await message_unit.DeleteMessage(discord_message, delay_seconds=5)
         ```

#### Notes:
- **Initialization Process**:
  - The system uses `INIT_PHRASE` to initialize channels by setting their IDs based on passwords.
  - Once all channels are initialized, the system is ready to process messages.
- **Webhook Communication**:
  - The `WebhookSend` function is used to send messages, embeds, and files to Discord webhooks.

---

### `progress_lib.py`
**Purpose**: Tracks the progress of models and datasets.

#### Status:
- **Deprecated**: This library is not updated to the system standard and is not included in `anomalib_train` or `anomalib_test`.
- **Modification**: It can be modified to align with the current system, but it is not actively maintained.

#### Classes:
- **`ProgressUnit`**:
  - **Attributes**:
    - `dataset_type_progress_`: Current dataset type.
    - `model_type_progress_`: Current model type.
    - `file_path_`: Path to the progress file.
    - `dataset_dict_`: Dictionary mapping dataset type strings to enums.
    - `model_dict_`: Dictionary mapping model type strings to enums.
    - `progression_matrix_`: Matrix tracking progress for datasets and models.
  - **Methods**:
    - **`write_progress`**: Writes the current progress to the progress file.
    - **`update_progress`**: Updates the current progress of the program.
    - **`read_progress`**: Reads the progress from the progress file.
    - **`matrix_gen`**: Generates the matrix of progress.
    - **`new_progress`**: Resets the progress of the program.
    - **`advanced_one`**: Advances the progress of the program by one step.
  - **Purpose**: Manages and tracks progress for datasets and models.

#### Notes:
- **Usage**: This library is not integrated into the main training or testing workflows (`anomalib_train` or `anomalib_test`).
- **Recommendation**: Consider updating or replacing this library to meet the current system standards.

#### Example:
```python
progress_unit = ProgressUnit()
progress_unit.read_progress()
progress_unit.update_progress(
    DatasetUnit.MVTecDatasetTypeEnum.bottle_,
    AnomalyModelUnit.AnomalyModelTypeEnum.padim_
)
progress_unit.write_progress()
```

---

### `pycaret_lib.py`
**Purpose**: Implements traditional anomaly detection models using the PyCaret library.

#### Classes:
1. **`PyCaretModelUnit`**:
   - **Purpose**: Provides a framework for training, evaluating, and predicting anomalies using PyCaret models.
   - **Enums**:
     - **`ModelTypeFlag`**:
       - **Purpose**: Enum for different types of anomaly detection models.
       - **Attributes**:
         - `abod_`: Angle-based Outlier Detection.
         - `cluster_`: Clustering-Based Local Outlier.
         - `cof_`: Connectivity-Based Outlier Factor.
         - `histogram_`: Histogram-based Outlier Detection.
         - `iforest_`: Isolation Forest.
         - `knn_`: k-Nearest Neighbors Detector.
         - `lof_`: Local Outlier Factor.
         - `svm_`: One-class SVM detector.
         - `pca_`: Principal Component Analysis.
         - `mcd_`: Minimum Covariance Determinant.
         - `sod_`: Subspace Outlier Detection.
         - `sos_`: Stochastic Outlier Selection.
         - `optimal_`: Combination of all models except `mcd_`.
       - **Example**:
         ```python
         model_type = PyCaretModelUnit.ModelTypeFlag.knn_
         ```
     - **`PlotTypeFlag`**:
       - **Purpose**: Enum for different types of plots for anomaly detection models.
       - **Attributes**:
         - `tsne_`: t-Distributed Stochastic Neighbor Embedding.
         - `umap_`: Uniform Manifold Approximation and Projection.
       - **Example**:
         ```python
         plot_type = PyCaretModelUnit.PlotTypeFlag.tsne_
         ```
   - **Attributes**:
     - `model_`: Internal PyCaret model instance.
     - `ModelTypeFlagName`: Dictionary mapping `ModelTypeFlag` to model names.
     - `PlotTypeFlagName`: Dictionary mapping `PlotTypeFlag` to plot names.
   - **Methods**:
     - **`Train`**:
       - **Purpose**: Trains the model using a dataset.
       - **Args**:
         - `data (DataFrame)`: Dataset for training.
         - `model_type (ModelTypeFlag)`: Type of model to train.
         - `model_path (Optional[str])`: Path to load an existing model.
       - **Example**:
         ```python
         model = PyCaretModelUnit()
         model.Train(data=train_data, model_type=PyCaretModelUnit.ModelTypeFlag.knn_)
         ```
     - **`Evaluate`**:
       - **Purpose**: Evaluates the trained model.
       - **Example**:
         ```python
         model.Evaluate()
         ```
     - **`Predict`**:
       - **Purpose**: Predicts anomalies in a dataset.
       - **Args**:
         - `data (DataFrame)`: Dataset for prediction.
       - **Returns**: A `DataFrame` with predictions.
       - **Example**:
         ```python
         predictions = model.Predict(data=test_data)
         ```
     - **`Results`**:
       - **Purpose**: Saves prediction results to a CSV file.
       - **Args**:
         - `data (DataFrame)`: Dataset for predictions.
         - `name (str)`: Name of the output CSV file.
       - **Example**:
         ```python
         model.Results(data=test_data, name="test_results")
         ```
     - **`EvaluationMetrics`**:
       - **Purpose**: Evaluates the model using test data.
       - **Args**:
         - `good (DataFrame)`: Good test data.
         - `defective (DataFrame)`: Defective test data.
         - `name (str)`: Name of the model for evaluation.
       - **Example**:
         ```python
         model.EvaluationMetrics(good=test_good, defective=test_defective, name="knn_model")
         ```
     - **`Plot`**:
       - **Purpose**: Plots the model using the specified plot type.
       - **Args**:
         - `plot_type (PlotTypeFlag)`: Type of plot to generate.
       - **Example**:
         ```python
         model.Plot(plot_type=PyCaretModelUnit.PlotTypeFlag.tsne_)
         ```
     - **`Save`**:
       - **Purpose**: Saves the trained model to a file.
       - **Args**:
         - `model_name (str)`: Name of the file to save the model.
       - **Example**:
         ```python
         model.Save(model_name="knn_model")
         ```

#### Notes:
- **PyCaret Integration**: This library uses PyCaret for anomaly detection, providing a low-code solution for training and evaluating models.
- **Supported Models**: Refer to the [PyCaret Documentation](https://pycaret.readthedocs.io/en/stable/api/anomaly.html) for details on supported models.

---

### `util_lib.py`
**Purpose**: Provides helper functions and utility classes.

#### Functions:
- **`Deprecated`**: Marks a function as deprecated.
- **`Unused`**: Marks variables as used to avoid warnings.
- **`TimeIt`**: Times the execution of a function.

#### Enums:
1. **`ColorCode`**:
   - **Purpose**: Enum for terminal text colors.
   - **Attributes**:
     - `red_`, `green_`, `yellow_`, `blue_`, `purple_`, `cyan_`, `white_`, `end_`: Color codes for terminal text.
   - **Example**:
     ```python
     print(ColorCode.red_, "Error", ColorCode.end_)
     ```

#### Classes:
1. **`Color`**:
   - **Purpose**: Provides utilities for printing colored text in the terminal.
   - **Methods**:
     - **`Print`**:
       - **Purpose**: Prints colored text.
       - **Args**:
         - `color (ColorCode)`: The color to use.
         - `text (str)`: The text to print.
       - **Example**:
         ```python
         Color.Print(ColorCode.red_, "Error")
         ```

2. **`Size`**:
   - **Purpose**: Represents 2D dimensions.
   - **Attributes**:
     - `width_`: Width of the size.
     - `height_`: Height of the size.
   - **Methods**:
     - Arithmetic operations (`Add`, `Sub`, `Mul`, etc.).
     - Comparison operations (`__eq__`, `__lt__`, etc.).
   - **Example**:
     ```python
     size = Size(10, 20)
     print(size.Add(5))  # Size(width=15, height=25)
     ```

3. **`Point`**:
   - **Purpose**: Represents 2D coordinates.
   - **Attributes**:
     - `x_`: X-coordinate.
     - `y_`: Y-coordinate.
   - **Methods**:
     - Arithmetic operations (`Add`, `Sub`, `Mul`, etc.).
     - Comparison operations (`__eq__`, `__lt__`, etc.).
   - **Example**:
     ```python
     point = Point(10, 20)
     print(point.Add(5))  # Point(x=15, y=25)
     ```

4. **`Rect`**:
   - **Purpose**: Represents a 2D rectangle.
   - **Attributes**:
     - `size_`: Size of the rectangle.
     - `point_`: Top-left corner of the rectangle.
   - **Methods**:
     - Arithmetic operations (`Add`, `Sub`, `Mul`, etc.).
     - Comparison operations (`__eq__`, `__lt__`, etc.).
   - **Example**:
     ```python
     rect = Rect(10, 20, 5, 5)
     print(rect.Add(5))  # Rect(size=Size(width=15, height=25), point=Point(x=10, y=10))
     ```

5. **`ValidationMixin`**:
   - **Purpose**: Provides validation methods for ensuring type safety and consistency.
   - **Methods**:
     - **`ValidateSize`**: Validates the dimensions of a `Size` object.
     - **`ValidatePoint`**: Validates the coordinates of a `Point` object.
   - **Example**:
     ```python
     class MyClass(ValidationMixin):
         def __init__(self, size: Size):
             self.ValidateSize(size)
     ```

#### Notes:
- **Validation**: The `Size`, `Point`, and `Rect` classes include validation methods to ensure type safety and consistency.
- **Usage**: These utility classes and functions are designed to be reusable across the project.
