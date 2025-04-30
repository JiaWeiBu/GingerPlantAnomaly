# Training and Testing

[Back to Main README](./README.md)

## Overview
This repository includes training and testing scripts for anomaly detection in ginger plants. Currently, **Anomalib** is the only fully implemented and tested framework for both training and testing.

### Key Features of Anomalib:
1. **Training Modes**: Supports both synchronous and asynchronous training.
2. **Testing**: Fully implemented testing pipeline.
3. **Administrator Mode**: Training requires administrator privileges to ensure proper execution.
4. **Usage Options**: Can be run as a standalone script or used as an API.

---

## How It Works
### Training
The training process involves:
1. Loading the dataset (train, test_good, and test_defective).
2. Training the model using the specified anomaly detection algorithm.
3. Saving the trained model to the specified directory.

### Testing
The testing process involves:
1. Loading the trained model.
2. Evaluating the model on test images.
3. Generating results, including metrics and visualizations.

---

## How to Use

### Training
#### Running as a Script
1. Ensure you have administrator privileges.
2. Run the `anomalib_train.py` script:
   ```bash
   python anomalib_train.py
   ```

#### Using as an API
You can use the `AnomalibTrain` class directly in your Python code:
```python
from anomalib_train import AnomalibTrain, TrainObject, TrainPathObject, ImageInfoObject
from classes.util_lib import Size
from classes.anomalib_lib import AnomalyModelUnit

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
        colour_mode='rgb',
        name='plant'
    )
)
model_type_flag = AnomalyModelUnit.ModelTypeFlag.padim_

anomalib_train = AnomalibTrain(param=train_object, model_type_flag=model_type_flag, logger_async=False, logger_instance=None, logger_instance_async=None)
anomalib_train.Run()
```

#### Asynchronous Training
For asynchronous training, use the `RunAsync` method:
```python
await anomalib_train.RunAsync()
```

---

### Testing
#### Running as a Script
Run the `anomalib_test.py` script:
```bash
python anomalib_test.py
```

#### Using as an API
You can use the `AnomalibTest` class directly in your Python code:
```python
from anomalib_test import AnomalibTest, ModelPathUnit

model_path_unit = ModelPathUnit()
anomalib_test = AnomalibTest()
anomalib_test.Setup(model_path=model_path_unit.ModelPath(types=ModelPathUnit.ModelTypeEnum.cflow_, week=ModelPathUnit.ModelWeekEnum.week3_))
results = anomalib_test.Evaluate(image_path="path/to/test/images")

for img, attributes in results:
    img.show()
    print(attributes)
```

---

## Notes
1. **Administrator Privileges**: Training with `anomalib_train.py` requires administrator mode. Ensure you run the script with elevated privileges.
2. **Dataset Structure**: Ensure the dataset is organized as follows:
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
3. **Model Save Path**: Trained models will be saved in the `models` directory.
4. **Training and Testing Modes**:
   - **Training**: Supports both asynchronous and non-asynchronous modes. Due to administrator privileges, training can bypass threading restrictions. It is recommended to manage training using a Flask application to handle the required loops and privileges effectively.
   - **Testing**: Does not require asynchronous handling and can be directly called in the main loop.

---

## Summary
- Use `anomalib_train.py` for training and `anomalib_test.py` for testing.
- Both scripts can be run directly or used as APIs in your Python projects.
- Ensure administrator privileges for training.
- Anomalib supports both synchronous and asynchronous training modes.
- Use Flask to manage training for better control over privileges and threading.
