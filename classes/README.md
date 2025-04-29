# Class Documentation

[Back to Main README](../README.md)

## Table of Contents
- [Overview](#overview)
- [anomalib_lib.py](#anomalib_libpy)
- [dataset_lib.py](#dataset_libpy)
- [discord_lib.py](#discord_libpy)
- [flask_lib.py](#flask_libpy)
- [general_lib.py](#general_libpy)
- [message_lib.py](#message_libpy)
- [progress_lib.py](#progress_libpy)
- [util_lib.py](#util_libpy)

## Overview
This folder contains the core classes and utility functions used in the GingerPlantAnomaly project. Each file serves a specific purpose, as described below.

---

### `anomalib_lib.py`
**Purpose**: Implements Anomalib-based anomaly detection models.

#### Classes:
- **`AnomalyModelUnit`**:
  - **Attributes**:
    - `ModelTypeFlag`: Enum for model types.
    - `VALID_MODELS_DICT`: Dictionary of valid models.
    - `MODELS_PARAMS_DICT`: Dictionary of model parameters.
    - `model_`: Internal Anomalib model.
    - `engine_`: Internal Anomalib engine.
  - **Methods**:
    - `Train`: Trains the model using a dataset.
    - `Evaluate`: Evaluates the model.
    - `Predict`: Predicts anomalies in a dataset.
    - `Save`: Saves the trained model.
    - `ModelValid`: Checks if a model is valid.
  - **Purpose**: Provides a framework for training, evaluating, and predicting using Anomalib models.

---

### `dataset_lib.py`
**Purpose**: Handles dataset loading, preprocessing, and management.

#### Classes:
- **`ImageUnit`**:
  - **Attributes**:
    - `ColorModeEnum`: Enum for image color modes.
    - `ColorConversionEnum`: Enum for color conversions.
    - `ImageInterpolationEnum`: Enum for resizing interpolation methods.
  - **Methods**:
    - `LoadImage`: Loads an image from a file.
    - `SaveImage`: Saves an image to a file.
    - `ResizeImage`: Resizes an image.
    - `ConvertColor`: Converts the color of an image.
    - `CropImage`: Crops an image.
    - `ShowImage`: Displays an image.
  - **Purpose**: Provides utilities for image processing.

- **`DatasetUnit`**:
  - **Attributes**:
    - `MVTecDatasetTypeEnum`: Enum for MVTec dataset types.
    - `MVTecDatasetTypeAnomalyEnum`: Enum for MVTec dataset anomalies.
    - `MVTecDataset`: Dictionary mapping dataset types to anomalies.
    - `images_`: List of loaded images.
    - `images_name_`: List of image names.
  - **Methods**:
    - `ClearDataset`: Clears the dataset.
    - `LoadImages`: Loads images from a directory.
    - `LoadImagesResize`: Loads and resizes images.
    - `AnomalibLoadFolder`: Loads a dataset for Anomalib.
  - **Purpose**: Manages dataset operations, including loading and preprocessing.

---

### `discord_lib.py`
**Purpose**: Manages Discord bot messages and interactions.

#### Classes:
- **`MessageObject`**:
  - **Attributes**:
    - `embed_`: Embed object for Discord messages.
    - `message_`: Text message content.
    - `file_`: File object for attachments.
  - **Methods**:
    - `SetMessage`: Sets the message content.
    - `CreateEmbed`: Creates an embed object.
    - `EmbedSetFooter`: Sets the footer for the embed.
    - `EmbedAddField`: Adds a field to the embed.
    - `EmbedSetImage`: Sets an image for the embed.
    - `EmbedSetThumbnail`: Sets a thumbnail for the embed.
    - `SetFile`: Attaches a file to the message.
  - **Purpose**: Provides utilities for creating and managing Discord messages.

---

### `flask_lib.py`
**Purpose**: Implements a Flask-based API for managing routes.

#### Functions:
- **`Callback`**: Registers a generic route.
- **`Get`**: Registers a GET route.
- **`Post`**: Registers a POST route.
- **`GetPost`**: Registers a route for both GET and POST methods.

#### Flask App:
- **`APP`**: Flask application instance.
- **Purpose**: Provides an API for interacting with the project.

---

### `general_lib.py`
**Purpose**: Provides utility classes for managing paths, image information, and training/testing configurations.

#### Classes:
- **`PredictPathObject`**:
  - **Attributes**:
    - `root_`: Root path for prediction.
    - `model_`: Path to the model.
    - `test_good_`: Path to good test data.
    - `test_defective_`: Path to defective test data.
  - **Purpose**: Manages paths for prediction tasks.

- **`ImageInfoObject`**:
  - **Attributes**:
    - `size_`: Size of the image.
    - `colour_mode_`: Colour mode of the image.
    - `name_`: Name of the image.
  - **Purpose**: Stores metadata about an image.

- **`TrainPathObject`**:
  - **Attributes**:
    - `root_`: Root path for training.
    - `train_`: Paths to training data.
    - `test_good_`: Paths to good test data.
    - `test_defective_`: Paths to defective test data.
    - `model_save_`: Path to save the model.
  - **Purpose**: Manages paths for training tasks.

- **`TrainObject`**:
  - **Attributes**:
    - `path_`: Instance of `TrainPathObject`.
    - `image_info_`: Instance of `ImageInfoObject`.
  - **Purpose**: Combines training paths and image metadata.

- **`TestPathObject`**:
  - **Attributes**:
    - `root_`: Root path for testing.
    - `test_good_`: Paths to good test data.
    - `test_defective_`: Paths to defective test data.
    - `test_mask_`: Paths to test masks.
  - **Purpose**: Manages paths for testing tasks.

- **`TestObject`**:
  - **Attributes**:
    - `path_`: Instance of `TestPathObject`.
    - `image_info_`: Instance of `ImageInfoObject`.
  - **Purpose**: Combines testing paths and image metadata.

---

### `message_lib.py`
**Purpose**: Manages Discord bot messages and interactions.

#### Classes:
- **`MessageUnit`**:
  - **Attributes**:
    - `channel_object_dict_`: Dictionary of channel objects.
    - `keyword_`: Keyword for bot initialization.
  - **Methods**:
    - `RegisterChannelObject`: Registers a channel object.
    - `SetChannelID`: Sets the channel ID.
    - `GetResponse`: Gets a response for a message.
    - `InitRoutine`: Initializes the bot.
  - **Purpose**: Handles Discord bot message routing and responses.

---

### `progress_lib.py`
**Purpose**: Tracks the progress of models and datasets.

#### Classes:
- **`ProgressUnit`**:
  - **Attributes**:
    - `dataset_type_progress_`: Current dataset type.
    - `model_type_progress_`: Current model type.
    - `progression_matrix_`: Matrix tracking progress.
  - **Methods**:
    - `write_progress`: Writes progress to a file.
    - `read_progress`: Reads progress from a file.
    - `update_progress`: Updates the current progress.
    - `matrix_gen`: Generates a progress matrix.
    - `new_progress`: Resets progress.
  - **Purpose**: Manages and tracks progress for datasets and models.

---

### `util_lib.py`
**Purpose**: Provides helper functions and utility classes.

#### Functions:
- **`Deprecated`**: Marks a function as deprecated.
- **`Unused`**: Marks variables as used to avoid warnings.
- **`TimeIt`**: Times the execution of a function.

#### Classes:
- **`Color`**:
  - **Attributes**:
    - `ColorCode`: Enum for terminal text colors.
  - **Methods**:
    - `Print`: Prints colored text.
  - **Purpose**: Provides utilities for printing colored text.

- **`Size`**:
  - **Attributes**:
    - `width_`: Width of the size.
    - `height_`: Height of the size.
  - **Methods**:
    - Arithmetic operations (`Add`, `Sub`, etc.).
    - Comparison operations (`__eq__`, `__lt__`, etc.).
  - **Purpose**: Represents 2D dimensions.
