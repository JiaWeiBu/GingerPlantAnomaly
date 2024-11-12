from typing import Optional
from anomalib.data.image.folder import Folder
from anomalib import TaskType
from anomalib.models import Draem, AnomalyModule
from anomalib.models.components.feature_extractors import BackboneParams
from anomalib.engine import Engine
from anomalib.utils.normalization import NormalizationMethod
from lightning.pytorch.callbacks.early_stopping import EarlyStopping

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
        num_workers=2,
        task=TaskType.CLASSIFICATION    
    )
    datamodule.setup()
    return datamodule

@TimeIt
def train_model(engine : Engine, model : AnomalyModule, datamodule : Folder):
    engine.fit(model=model, datamodule=datamodule)

@TimeIt
def test_model(engine : Engine, model : AnomalyModule, datamodule : Folder):
    test_result = engine.test(model=model, datamodule=datamodule)
    return test_result

@TimeIt
def main():
    datamodule = read_image(normal=["train/good","test/good"], abnormal=["test/broken_large", "test/broken_small", "test/contamination"], ratio=0, name="train")

    # model = Padim(
    #     backbone="resnet18",
    #     layers=['layer1', 'layer2', 'layer3'],
    #     pre_trained=True,
    #     n_features=100,
    # )

    model = Draem(
        enable_sspcab=True,
        sspcab_lambda=0.1,
        anomaly_source_path=None,
        beta=(0.1, 1.0)
    )
    
    early_stopping_callback = EarlyStopping(
        monitor="train_loss_epoch",
        patience=5,
        mode="min",
        verbose=True,
    )

    engine = Engine(
        normalization=NormalizationMethod.MIN_MAX,
        threshold="F1AdaptiveThreshold",
        task=TaskType.CLASSIFICATION,
        image_metrics=["AUROC", "AUPR"],
        max_epochs=100,
        callbacks=[early_stopping_callback],
        accelerator="auto",
        devices="auto",
        #check_val_every_n_epoch=5,
    )
    train_model(engine, model, datamodule)

    test_result = test_model(engine, model, datamodule)

if __name__ == '__main__':
    main()
