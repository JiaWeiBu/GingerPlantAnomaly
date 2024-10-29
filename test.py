from classes.model_lib import ModelType, PlotType, ModelUnit
from pycaret.datasets import get_data # type: ignore
from classes.dataset_lib import DatasetUnit, ImageUnit, ColorMode
from classes.util_lib import Size
from pandas import DataFrame

def main():
    # Load Data
    train_module = DatasetUnit()
    train_module.LoadImagesResize("./datasets/ds1/train", ColorMode.grayscale_, Size(64, 64))

    test_good_module = DatasetUnit()
    test_good_module.LoadImagesResize("./datasets/ds1/test/good", ColorMode.grayscale_, Size(64, 64))
    
    test_defective_module = DatasetUnit()
    test_defective_module.LoadImagesResize("./datasets/ds1/test/defective", ColorMode.grayscale_, Size(64, 64))

    train = DataFrame(train_module.images_)
    test_good = DataFrame(test_good_module.images_)
    test_defective = DataFrame(test_defective_module.images_)

    # Train Model
    # For each ModelType in ModelType Enum, train the model and save it
    with open('./results/result.csv', 'w') as f:
        f.write("Model,Accuracy,Precision,Recall,F1-score\n")
    
    total_model = len(ModelType)
    count = 1
    for model_type in ModelType:
        try:
            print(f"Training {model_type.value} model {count}/{total_model}")
            model = ModelUnit()
            model.Train(data=train, model_type=model_type)

            #model.Evaluate()
            #model.Plot(PlotType.tsne_)
            model.Save(f"{model_type.value}_model_1")
            # model.Results(test_good, "knn_model_good_1")
            # model.Results(test_defective, "knn_model_defective_1")
            model.EvaluationMetrics(test_good, test_defective, model_type.value)

            count += 1
        except Exception as e:
            print(f"Error training {model_type.value} model: {e}")
            continue


if __name__ == "__main__":
    main()