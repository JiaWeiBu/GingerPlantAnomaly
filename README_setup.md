# Setup and Dataset

[Back to Main README](./README.md)

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/GingerPlantAnomaly.git
   cd GingerPlantAnomaly
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dataset
1. Download the MVTec dataset or your custom dataset.
2. Organize the dataset into the following structure:
   ``` 
   dataset/
   ├── train/
   ├── test_good/
   └── test_defective/
   ```
3. Update the dataset paths in your training configuration.
