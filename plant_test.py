import cv2
import os
from classes.pycaret_lib import PyCaretModelUnit # type: ignore
from classes.dataset_lib import DatasetUnit, ImageUnit
from classes.util_lib import Size, Unused
import pandas as pd

def main():
    image_size = Size(64, 64)
    dataset_path = "./datasets"

    image_ = cv2.imread(f"{dataset_path}/plant/week3/top/00001.jpg")
    image2_ = cv2.imread(f"{dataset_path}/plant/week3/top/00002.jpg")
    image_ = cv2.resize(image_, (image_size.width_, image_size.height_))
    image2_ = cv2.resize(image2_, (image_size.width_, image_size.height_))

    images = []
    images.append(image_.flatten())
    images.append(image2_.flatten())
    
    df = pd.DataFrame(images)

    model = PyCaretModelUnit()
    model.Train(data=df, model_type=PyCaretModelUnit.PyCaretModelTypeEnum.abod_)
    model.EvaluationMetrics(good=df, defective=pd.DataFrame(), name="plant")


if __name__ == "__main__":
    main()