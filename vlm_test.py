# Load model directly
from transformers import AutoProcessor, AutoModelForImageTextToText
from PIL import Image
from typing import Any

class PromptObject:
    def __init__(self, image, labels, path):
        self.image_ = image
        self.labels_ : str = labels
        self.path_ : str = path

def ConversationBinder(prompt : PromptObject) -> list[dict[str, Any]]:
    return [
        {
            "role": "user",
            "content" : [
                {"type": "text", "text": prompt.labels_},
                {"type": "image"},
            ],
        },
    ]


def main():
    GOOD_IMAGE_PATH = "./datasets/bottle/test/good/000.png"
    DEFECTIVE_IMAGE_PATH = "./datasets/bottle/test/broken_large/000.png"
    DEFECTIVE_IMAGE_PATH2 = "./datasets/bottle/test/broken_large/001.png"
    FIRST_PROMPT = "You are given an image. It is either normal or anomalous. \
                    First say 'YES' if the image is anomalous, or 'NO' if it is normal.\n \
                    Then give the reason for your decision.\n \
                    For example, 'YES: The image has a crack on the wall.'"

    processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-vicuna-7b-hf")
    model = AutoModelForImageTextToText.from_pretrained("llava-hf/llava-v1.6-vicuna-7b-hf")
    model.to("cuda")

    image_path_list = [GOOD_IMAGE_PATH, DEFECTIVE_IMAGE_PATH, DEFECTIVE_IMAGE_PATH2]

    for image_path in image_path_list:
        image = Image.open(image_path)
        prompt = processor.apply_chat_template(conversation=ConversationBinder(PromptObject(image=image, labels=FIRST_PROMPT, path=image_path)))

        inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda")

        outputs = model.generate(**inputs)

        print(processor.decode(outputs[0], skip_special_tokens=True), "\n\n", image_path)
        print("------------------------------------------------------------")


if __name__ == "__main__":
    main()