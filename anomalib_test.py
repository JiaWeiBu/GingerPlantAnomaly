from typing import Optional
from anomalib.data.image.folder import Folder
from anomalib import TaskType
from anomalib.models import Padim
from anomalib.models.components.feature_extractors import BackboneParams
from anomalib.engine import Engine
from anomalib.utils.normalization import NormalizationMethod
from classes.util_lib import Color, TimeIt



@TimeIt
def read_image(*, normal : list[str], abnormal : Optional[list[str]], ratio : float , name : str) -> Folder:
    datamodule = Folder(
        name=name,
        root="datasets/bottle",
        normal_dir=normal,
        abnormal_dir=abnormal,
        normal_split_ratio=ratio,
        image_size=(64, 64),
        train_batch_size=32,
        eval_batch_size=32,
        num_workers=8,
        task=TaskType.CLASSIFICATION    
    )
    datamodule.setup()
    return datamodule

@TimeIt
def train_model(engine : Engine, model : Padim, datamodule : Folder):
    engine.fit(model=model, datamodule=datamodule)

@TimeIt
def test_model(engine : Engine, model : Padim, datamodule : Folder):
    test_result = engine.test(model=model, datamodule=datamodule)
    return test_result

@TimeIt
def main():
    train_datamodule = read_image(normal=["train/good"], abnormal=None, ratio=0, name="train")
    test_datamodule = read_image(normal=["test/good"], abnormal=["test/broken_large", "test/broken_small", "test/contamination"], ratio=1, name="test")

    model = Padim(
        backbone="resnet18",
        layers=['layer1', 'layer2', 'layer3'],
        pre_trained=True,
        n_features=100,
    )

    engine = Engine(
        normalization=NormalizationMethod.MIN_MAX,
        threshold="F1AdaptiveThreshold",
        task=TaskType.CLASSIFICATION,
        image_metrics=["AUROC"],
    )
    train_model(engine, model, train_datamodule)

    test_result = test_model(engine, model, test_datamodule)

if __name__ == '__main__':
    main()
