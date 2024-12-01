# Load model directly
from ollama import generate, GenerateResponse, Options
from os import listdir
from os.path import isfile, join
from time import time
from functools import partial
from typing import Callable
from base64 import b64encode
from PIL import Image

PROMPT = "You are given an image. It is either normal or anomalous. \
        Plaese answer only \"Yes\" or \"No\", No explanation needed.\
        For example : Yes\
        The image shown is a bottle. Is it anomalous?"

TEST_PROMPT = "Describe this image"

MODEL_NAME = "llava-llama3"

def UnloadModel():
    generate(model=MODEL_NAME, keep_alive=0)
    print(f"Model {MODEL_NAME} unloaded")

#decorator to time the function
def timeit(func):
    def timed(*args, **kw):
        ts = time()
        result = func(*args, **kw)
        te = time()
        print(f"Time taken: {te-ts}")
        return result
    return timed

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

def DirImages(path : str) -> list[str]:
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def contains_yes_or_no(input_string):
    # Convert the string to lowercase and check for the words
    input_string = input_string.lower()
    return 'yes' in input_string or 'no' in input_string

def Generate(images_path : list[str], anomaly: bool) -> tuple[int, int]:
    count = 0
    total = 0
    patient = 0
    for image_path in images_path:
        loop = True

        with open(image_path, "rb") as image_file:
            image_base64 = b64encode(image_file.read()).decode("utf-8")

        while(loop):
            print("\n------------------------------------------------------------\n")
            result : GenerateResponse = generate(
                model=MODEL_NAME,
                prompt=PROMPT,
                images=[image_base64],
                options={"num_predict": 2}
            ) # type: ignore

            if contains_yes_or_no(result['response']):
                loop = False
                patient = 0
            else:
                if patient > 3:
                    UnloadModel()
                print(f"Time wasted: {result['total_duration']/1e9:.2f} seconds")
                print(f"Invalid response: {result['response']}")
                patient += 1
                continue

            print(f"Image: {image_path}")
            print(f"Result: {result['response']}")
            print(f"Time taken: {result['total_duration']/1e9:.2f} seconds")

            if anomaly:
                count += 'yes' in result['response'].lower()
            else:
                count += 'no' in result['response'].lower()
            total += 1

    print(f"Total: {total}")
    print(f"Correct: {count}")
    print(f"Accuracy: {count/total}")
    return count, total

def main():
    types = "pill"
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    print("Good")
    #Generate(DirImages("datasets/bottle/test/good"), False)
    amount, total = Generate(DirImages(f"datasets/{types}/test/good"), False)
    TN += amount
    FP += total - amount
    amount, total = Generate(DirImages(f"datasets/{types}/train/good"), False)
    TN += amount
    FP += total - amount
    print("\n\n\n")
    print("Anomalous")
    anomaly_types = ["color", "combined", "contamination", "crack", "faulty_imprint", "pill_type", "scratch"]
    for anomaly_type in anomaly_types:
        print(anomaly_type)
        amount, total = Generate(DirImages(f"datasets/{types}/test/{anomaly_type}"), True)
        TP += amount
        FN += total - amount
        print("\n\n\n")

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * (precision * recall) / (precision + recall)
    
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1: {f1}")
    UnloadModel()

if __name__ == "__main__":
    main()