from ultralytics import YOLO
from enum import Enum, auto
import mlflow
from os import listdir
from os.path import isfile, join
import cv2

MODEL_PATH : str = "models/segmentation"
DATABASE_PATH : str = "datasets/segmentation"
TEST_PATH_60 : str = "datasets/re_plant/good/60"
TEST_PATH_TOP : str = "datasets/re_plant/good/top"

def DirImages(path : str) -> list[str]:
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def DirImagesNum(path : str, num : int) -> list[str]:
    temp_list = []
    counter = 0
    for f in listdir(path):
        if isfile(join(path, f)):
            temp_list.append(join(path, f))
            counter += 1
            if counter == num:
                break
    return temp_list

class ModelSegmentationSize(Enum):
    nano_ = auto()
    small_ = auto()
    medium_ = auto()
    large_ = auto()
    extra_large_ = auto()

ModelSegmentationPath : dict[ModelSegmentationSize, str] = {
    ModelSegmentationSize.nano_ : f"{MODEL_PATH}/yolo11n-seg.pt",
    ModelSegmentationSize.small_ : f"{MODEL_PATH}/yolo11s-seg.pt",
    ModelSegmentationSize.medium_ : f"{MODEL_PATH}/yolo11m-seg.pt",
    ModelSegmentationSize.large_ : f"{MODEL_PATH}/yolo11l-seg.pt",
    ModelSegmentationSize.extra_large_ : f"{MODEL_PATH}/yolo11x-seg.pt"
}

def main():
    for model_size in [ModelSegmentationSize.medium_]:
        print(f"Model Size: {model_size}")
        print(f"Model Path: {ModelSegmentationPath[model_size]}")
        model = YOLO(ModelSegmentationPath[model_size])
        print("Model Loaded")
        mlflow.set_tracking_uri("file:///C:/Users/aaron/Desktop/repo/GingerPlantAnomaly/runs/mlflow")
        model.train(
            # model = None,
            data = f"{DATABASE_PATH}/data.yaml",
            epochs = 100,
            patience = 10,
            device = 0,
            batch = -1, # -1 is 60% of GPU
            imgsz = 640,
            workers = 8,
        )

    test_path_60_5 = DirImagesNum(TEST_PATH_60, 10)
    test_path_top_5 = DirImagesNum(TEST_PATH_TOP, 10)

    for image_path in test_path_60_5:
        results = model(image_path)
        annotated_image = results[0].plot()
        cv2.imshow("Image", annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    for image_path in test_path_top_5:
        results = model(image_path)
        annotated_image = results[0].plot()
        cv2.imshow("Image", annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

    

if __name__ == "__main__":
    main()