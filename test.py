from classes.model_lib import ModelType, PlotType, Model
from pycaret.datasets import get_data # type: ignore

def main():
    knn_model = Model()
    data = get_data('anomaly')
    knn_model.Train(data=data, model_type=ModelType.KNN)
    #knn_model.evaluate()
    knn_model.Plot(PlotType.TSNE)
    knn_model.Save("knn_model_1")
    knn_model.Results(data, "knn_model_1")


if __name__ == "__main__":
    main()