# Setup and Dataset

[Back to Main README](./README.md)

## Setup

### Software Installation
1. **Install Python**:
   - Download and install Python version `3.11.9` from the [official Python website](https://www.python.org/).
   - Ensure that Python is added to your system's PATH during installation.

2. **Install Ollama** (if using Ollama VLM for anomaly detection):
   - Follow the installation instructions from the [Ollama website](https://ollama.com/).

3. **Install Git**:
   - Download and install Git from the [official Git website](https://git-scm.com/).

4. **Install GitHub Desktop** (optional):
   - Download and install GitHub Desktop from the [GitHub Desktop website](https://github.com/apps/desktop).

5. **Install a Virtual Environment Tool** (optional but recommended):
   - Use `venv` (comes with Python) or install `virtualenv`:
     ```bash
     pip install virtualenv
     ```

---

### Python Dependencies
1. Clone the repository:
   #### Using Git:
   ```bash
   git clone https://github.com/your-repo/GingerPlantAnomaly.git
   cd GingerPlantAnomaly
   ```

   #### Using GitHub Desktop:
   - Open GitHub Desktop.
   - Click on `File > Clone Repository`.
   - In the `URL` tab, paste the repository URL: `https://github.com/your-repo/GingerPlantAnomaly.git`.
   - Choose a local path to save the repository and click `Clone`.

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

### Dataset Preparation
1. **Download the Dataset**:
   - Use the MVTec dataset or your custom dataset.

2. **Organize the Dataset**:
   - Ensure the dataset is structured as follows:
     ```
     datasets/
         temp/
             train/
                 <normal_training_images>/ 
             good/
                 <normal_testing_images>/ 
             bad/
                 <defective_testing_images>/ 
     ```
   - Update the dataset paths in the `anomalib_train.py` file under the `TrainObject` initialization:
     ```python
     # filepath: c:\Repo\GingerPlantAnomaly\anomalib_train.py
     train_object = TrainObject(
         path=TrainPathObject(
             root='datasets/temp', 
             train=['train'], 
             test_good=['good'], 
             test_defective=['bad'], 
             model_save='models'
         ),
         image_info=ImageInfoObject(
             size=Size(width=256, height=256),
             colour_mode=ImageUnit.ColorModeEnum.rgb_,
             name='dataset_name'
         )
     )
     ```

3. **Dataset Notes**:
   - The dataset paths are configured in the `anomalib_train.py` file under the `TrainObject` initialization.
   - Ensure the dataset contains subdirectories for training (`train`), good test images (`good`), and defective test images (`bad`).
   - The `DatasetUnit.AnomalibLoadFolder` method in `dataset_lib.py` is responsible for loading the dataset. Refer to this method for advanced configurations.

---

### Configuration Details
1. **Patient Epoch**:
   - The `patient` variable is not used in the Anomalib-based system. Instead, ensure proper dataset structure and configurations in `anomalib_train.py` and `dataset_lib.py`.

2. **Number of Workers**:
   - The `num_workers` parameter is configured in the `DatasetUnit.AnomalibLoadFolder` method in `dataset_lib.py`:
     ```python
     # filepath: c:\Repo\GingerPlantAnomaly\classes\dataset_lib.py
     self.folder_ = Folder(
         ...existing code...
         num_workers=2,  # Adjust this value based on your system's capabilities
         ...existing code...
     )
     ```

3. **Batch Sizes**:
   - Training and evaluation batch sizes are set in the same method:
     ```python
     # filepath: c:\Repo\GingerPlantAnomaly\classes\dataset_lib.py
     self.folder_ = Folder(
         ...existing code...
         train_batch_size=32,  # Adjust training batch size
         eval_batch_size=32,   # Adjust evaluation batch size
         ...existing code...
     )
     ```

4. **Image Size**:
   - The default image size for resizing is configured in the `ImageInfoObject` in `anomalib_train.py`:
     ```python
     # filepath: c:\Repo\GingerPlantAnomaly\anomalib_train.py
     image_info=ImageInfoObject(
         size=Size(width=256, height=256),  # Update this size if needed
         colour_mode=ImageUnit.ColorModeEnum.rgb_,
         name='dataset_name'
     )
     ```

5. **Administrator Privileges**:
   - Training requires administrator mode to bypass threading restrictions. Ensure you run the training script with elevated privileges.

---

### Environment Variables
1. Create a `.env` file in the root directory with the following variables:
   ```env
   TOKEN_BOT_GITHUB=<your-bot-token>
   CHANNEL_WEBHOOK_LOG=<webhook-url-for-log-channel>
   CHANNEL_WEBHOOK_PREDICT=<webhook-url-for-predict-channel>
   CHANNEL_WEBHOOK_DEBUG=<webhook-url-for-debug-channel>
   CHANNEL_WEBHOOK_CLONE=<webhook-url-for-clone-channel>
   ```

2. Replace `<your-bot-token>` with the token you copied from the [Discord Developer Portal](https://discord.com/developers/docs/intro).

3. Replace `<webhook-url-for-*>` with the appropriate webhook URLs for your Discord channels.

**Note**: The `TOKEN_BOT_GITHUB` is used by the bot to authenticate and connect to Discord. Ensure this token is kept secure and not shared publicly.

---

### Setting Up Discord Bot

#### Creating a Discord Application
1. Go to the [Discord Developer Portal](https://discord.com/developers/docs/intro).
2. Log in with your Discord account.
3. Click on the **"New Application"** button.
4. Enter a name for your application and click **"Create"**.
5. Navigate to the **"Bot"** tab in the left-hand menu.
6. Click **"Add Bot"** and confirm by clicking **"Yes, do it!"**.
7. Copy the **Token** for your bot. This will be used in the `.env` file as `TOKEN_BOT_GITHUB`.

#### Creating Webhooks
1. Open your Discord server and navigate to the channel where you want to create a webhook.
2. Click on the channel name and select **"Edit Channel"**.
3. Go to the **"Integrations"** tab and click **"Create Webhook"**.
4. Set a name and optionally an avatar for the webhook.
5. Copy the **Webhook URL** and save it. This will be used in the `.env` file as:
   - `CHANNEL_WEBHOOK_LOG`
   - `CHANNEL_WEBHOOK_PREDICT`
   - `CHANNEL_WEBHOOK_DEBUG`
   - `CHANNEL_WEBHOOK_CLONE`

For more details, refer to the [Discord Webhooks Guide](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

#### Creating and Inviting the Bot
1. In the [Discord Developer Portal](https://discord.com/developers/docs/intro), go to your application.
2. Navigate to the **"OAuth2"** tab and select **"URL Generator"**.
3. Under **Scopes**, select **"bot"**.
4. Under **Bot Permissions**, select the permissions your bot needs (e.g., **"Send Messages"**, **"Read Messages"**, etc.).
5. Copy the generated URL and paste it into your browser.
6. Select the server where you want to add the bot and click **"Authorize"**.

For more details, refer to the [Discord.py Bot Guide](https://discordpy.readthedocs.io/en/stable/discord.html).

#### Setting the Bot Token
1. Open the `.env` file in the root directory of the project.
2. Add the following line to set the bot token:
   ```env
   TOKEN_BOT_GITHUB=<your-bot-token>
   ```
3. Replace `<your-bot-token>` with the token you copied from the [Discord Developer Portal](https://discord.com/developers/docs/intro).

**Note**: The `TOKEN_BOT_GITHUB` is used by the bot to authenticate and connect to Discord. Ensure this token is kept secure and not shared publicly.

---

### Running the Program
1. **Training**:
   - Run the training script:
     ```bash
     python anomalib_train.py
     ```
   - Alternatively, use the Flask API to manage training:
     ```bash
     python server.py
     ```
     Access the `/Train` endpoint to start training.

2. **Testing**:
   - Run the testing script:
     ```bash
     python anomalib_test.py
     ```

3. **Discord Bot**:
   - Start the Discord bot:
     ```bash
     python app.py
     ```

4. **Flask Server**:
   - Start the Flask server:
     ```bash
     python server.py
     ```
   - Use the `/PredictSetup` and `/Predict` endpoints for prediction tasks.

---

### Notes
1. **Flask for Training**:
   - Training is managed using Flask to handle asynchronous and synchronous loops effectively.
   - Flask ensures proper handling of administrator privileges and threading.

2. **Testing Simplicity**:
   - Testing does not require asynchronous handling and can be directly called in the main loop.

3. **Discord Bot**:
   - The bot provides an interactive UI for managing anomaly detection tasks.
   - Ensure the bot has the necessary permissions to read and send messages in the designated channels.

4. **Compatibility**:
   - This project uses **Anomalib version `1.2.0`**. The latest version (`2.0.0`) is not compatible with the current implementation.

---

## Summary
- Install Python `3.11.9` and required dependencies.
- Prepare the dataset in the specified structure.
- Configure environment variables in the `.env` file.
- Use Flask for training and testing or run scripts directly.
- Start the Discord bot for interactive anomaly detection management.
