from enum import Enum, unique, Flag, auto

from typing import Optional, Final, Any
from pandas import DataFrame

from anomalib.models.components import AnomalyModule
from anomalib.models import AiVad, Cfa, Cflow, Csflow, Draem, Dfkde, Dfm, Dsr, EfficientAd, Fastflow, Fre, Ganomaly, Padim, Patchcore, ReverseDistillation, Rkde, Stfpm, Uflow, VlmAd, WinClip, get_available_models
from anomalib.engine import Engine
from anomalib import TaskType, LearningType
from anomalib.loggers import AnomalibCometLogger, AnomalibMLFlowLogger, AnomalibTensorBoardLogger, AnomalibWandbLogger
from anomalib.models.components.classification import FeatureScalingMethod
from anomalib.models.image.reverse_distillation.anomaly_map import AnomalyMapGenerationMode
from anomalib.utils.normalization import NormalizationMethod
from anomalib.data.image.folder import Folder
from anomalib.deploy import ExportType
from anomalib.models.image.efficient_ad.torch_model import EfficientAdModelSize
from anomalib.models.image.rkde.region_extractor import RoiStage

from lightning.pytorch.callbacks.early_stopping import EarlyStopping

from classes.util_lib import Deprecated, TimeIt

class AnomalyModelUnit: 
    """
    Class for anomaly detection model unit.
    Each model will be trained using the dataset and the model will be saved.

    Enum:
        ModelTypeFlag : Enum for different types of anomaly detection models.
        AnomalibLoggerTypeEnum : Enum for different types of logger for anomaly detection models.
        AnomalibTaskTypeEnum : Enum for different types of task for anomaly detection models.
        AnomalibLearningTypeEnum : Enum for different types of learning for anomaly detection models
    
    Dictionary:
        VALID_MODELS_DICT : Dict[ModelTypeFlag, bool] : Dictionary for valid models.
        MODELS_PARAMS_DICT : Dict[ModelTypeFlag, Dict[str, Any]] : Dictionary for model parameters.

    Attributes:
        model_ : Optional[AnomalyModule] : Internal Anomalib model.
        engine_ : Optional[Engine] : Internal Anomalib engine.
        model_type_ : Optional[ModelTypeFlag] : Model for anomaly detection.
        image_metrics_ : list[str] : Image metrics for anomaly detection.
        task_ : Optional[AnomalibTaskTypeEnum] : Task for anomaly detection

    Methods:
        Setter : Set the model parameters.
        Train : Train the model using the dataset.
        Evaluate : Evaluate the model.
        Predict : Predict anomalies in the dataset.
        Save : Save the model.
        ModelValid : Check if the model is valid.

    Example:
    >>> model = AnomalyModelUnit()
    >>> model.Train(datamodule=datamodule)
    >>> model.Evaluate(datamodule=datamodule)
    >>> model.Predict(data=test)
    >>> model.Save(path="model")
    """

    @unique
    class ModelTypeFlag(Flag):
        """
        Enum for different types of anomaly detection models.

        Model from Anomalib
        ai_vad_ : Accurate and Interpretable Video Anomaly Detection
        cfa_ : Coupled-hypersphere-based Feature Adaptation
        cflow_ : Conditional Normalizing Flows
        csflow_ : Cross-Scale-Flows
        draem_ : Discriminatively Trained Reconstruction Anomaly Embedding Model
        dfkde_ : Deep Feature Kernel Density Estimation
        dfm_ : Deep Feature Modelling
        dsr_ : Dual Subspace Re-Projections
        efficient_ad_ : Efficient Anomaly Detection
        fastflow_ : Fast Flow Anomaly
        fre_ : Feature Reconstruction Error
        ganomaly_ :  Generative Adversarial Networks for Anomaly Detection
        padim_ : Patch Distribution Modeling
        patchcore_ : PatchCore
        reverse_distillation_ : Reverse Distillation
        rkde_ : Region-Based Kernel Density Estimation
        stfpm_ : Student-Teacher Feature Pyramid Matching
        uflow_ :  U-shaped Normalizing Flow
        vlm_ad_ : Visual Language Model for Anomaly Detection
        win_clip_ : Windowed-Based Contrastive Language-Image Pre-training
        """
        ai_vad_ = auto()
        cfa_ = auto()
        cflow_ = auto()
        csflow_ = auto()
        draem_ = auto()
        dfkde_ = auto()
        dfm_ = auto()
        dsr_ = auto()
        efficient_ad_ = auto()
        fastflow_ = auto()
        fre_ = auto()
        ganomaly_ = auto()
        padim_ = auto()
        patchcore_ = auto()
        reverse_distillation_ = auto()
        rkde_ = auto()
        stfpm_ = auto()
        uflow_ = auto()
        vlm_ad_ = auto()
        win_clip_ = auto()

    ModelTypeFlagName : Final[dict[ModelTypeFlag, Any]] = {
        ModelTypeFlag.ai_vad_ : AiVad,
        ModelTypeFlag.cfa_ : Cfa,
        ModelTypeFlag.cflow_ : Cflow,
        ModelTypeFlag.csflow_ : Csflow,
        ModelTypeFlag.draem_ : Draem,
        ModelTypeFlag.dfkde_ : Dfkde,
        ModelTypeFlag.dfm_ : Dfm,
        ModelTypeFlag.dsr_ : Dsr,
        ModelTypeFlag.efficient_ad_ : EfficientAd,
        ModelTypeFlag.fastflow_ : Fastflow,
        ModelTypeFlag.fre_ : Fre,
        ModelTypeFlag.ganomaly_ : Ganomaly,
        ModelTypeFlag.padim_ : Padim,
        ModelTypeFlag.patchcore_ : Patchcore,
        ModelTypeFlag.reverse_distillation_ : ReverseDistillation,
        ModelTypeFlag.rkde_ : Rkde,
        ModelTypeFlag.stfpm_ : Stfpm,
        ModelTypeFlag.uflow_ : Uflow,
        ModelTypeFlag.vlm_ad_ : VlmAd,
        ModelTypeFlag.win_clip_ : WinClip
    }

    VALID_MODELS_DICT: Final[dict[ModelTypeFlag, bool]] = {
        ModelTypeFlag.ai_vad_ : False,
        ModelTypeFlag.cfa_ : False,
        ModelTypeFlag.cflow_ : False,
        ModelTypeFlag.csflow_ : False,
        ModelTypeFlag.draem_ : True,
        ModelTypeFlag.dfkde_ : True,
        ModelTypeFlag.dfm_ : False,
        ModelTypeFlag.dsr_ : False,
        ModelTypeFlag.efficient_ad_ : False,
        ModelTypeFlag.fastflow_ : True,
        ModelTypeFlag.fre_ : False,
        ModelTypeFlag.ganomaly_ : True,
        ModelTypeFlag.padim_ : True,
        ModelTypeFlag.patchcore_ : True,
        ModelTypeFlag.reverse_distillation_ : True,
        ModelTypeFlag.rkde_ : False,
        ModelTypeFlag.stfpm_ : True,
        ModelTypeFlag.uflow_ : False,
        ModelTypeFlag.vlm_ad_ : False,
        ModelTypeFlag.win_clip_ : False

        # # set all models to True
        # ModelTypeFlag.ai_vad_ : False,
        # ModelTypeFlag.cfa_ : True,
        # ModelTypeFlag.cflow_ : True,
        # ModelTypeFlag.csflow_ : True,
        # ModelTypeFlag.draem_ : True,
        # ModelTypeFlag.dfkde_ : True,
        # ModelTypeFlag.dfm_ : True,
        # ModelTypeFlag.dsr_ : True,
        # ModelTypeFlag.efficient_ad_ : True,
        # ModelTypeFlag.fastflow_ : True,
        # ModelTypeFlag.fre_ : True,
        # ModelTypeFlag.ganomaly_ : True,
        # ModelTypeFlag.padim_ : True,
        # ModelTypeFlag.patchcore_ : True,
        # ModelTypeFlag.reverse_distillation_ : True,
        # ModelTypeFlag.rkde_ : True,
        # ModelTypeFlag.stfpm_ : True,
        # ModelTypeFlag.uflow_ : True,
        # ModelTypeFlag.vlm_ad_ : False,
        # ModelTypeFlag.win_clip_ : True            
    }

    MODELS_PARAMS_DICT: Final[dict[ModelTypeFlag, dict[str, Any]]] = {
        ModelTypeFlag.ai_vad_ : { 
            "box_score_thresh" : 0.7,
            "persons_only" : False,
            "min_bbox_area" : 100,
            "max_bbox_overlap" : 0.65,
            "enable_foreground_detections" : True,
            "foreground_kernel_size" : 3,
            "foreground_binary_threshold" : 18,
            "n_velocity_bins" : 1,
            "use_velocity_features" : True,
            "use_pose_features" : True,
            "use_deep_features" : True,
            "n_components_velocity" : 2,
            "n_neighbors_pose" : 1,
            "n_neighbors_deep" : 1
        },
        ModelTypeFlag.cfa_ : {
            "backbone" : "wide_resnet50_2",
            "gamma_c" : 1,
            "gamma_d" : 1,
            "num_nearest_neighbors" : 3,
            "num_hard_negative_features" : 3,
            "radius" : 1e-05
        },
        ModelTypeFlag.cflow_ : {
            "backbone" : "wide_resnet50_2",
            "layers" : ('layer2', 'layer3', 'layer4'),
            "pre_trained" : True,
            "fiber_batch_size" : 64,
            "decoder" : "freia-cflow",
            "condition_vector" : 128,
            "coupling_blocks" : 8,
            "clamp_alpha" : 1.9,
            "permute_soft" : False,
            "lr" : 0.0001
        },
        ModelTypeFlag.csflow_ : {
            "cross_conv_hidden_channels" : 1024,
            "n_coupling_blocks" : 4,
            "clamp" : 3,
            "num_channels" : 3
        },
        ModelTypeFlag.draem_ : {
            "enable_sspcab" : False,
            "sspcab_lambda" : 0.1,
            "anomaly_source_path" : None,
            "beta" : (0.1, 1.0)
        },
        ModelTypeFlag.dfkde_ : {
            "backbone" : "resnet18",
            "layers" : ('layer4',),
            "pre_trained" : True,
            "n_pca_components" : 16,
            "feature_scaling_method" : FeatureScalingMethod.SCALE,
            "max_training_points" : 40000
        },
        ModelTypeFlag.dfm_ : {
            "backbone" : "resnet50",
            "layer" : "layer3",
            "pre_trained" : True,
            "pooling_kernel_size" : 4,
            "pca_level" : 0.97,
            "score_type" : "fre"
        },
        ModelTypeFlag.dsr_ : {
            "latent_anomaly_strength" : 0.2,
            "embedding_dim" : 128,
            "num_embeddings" : 4096,
            "num_hiddens" : 128,
            "num_residual_layers" : 2,
            "num_residual_hiddens" : 64
        },
        ModelTypeFlag.efficient_ad_ : {#imagenet_dir='./datasets/imagenette', teacher_out_channels=384, model_size=EfficientAdModelSize.S, lr=0.0001, weight_decay=1e-05, padding=False, pad_maps=True
            "imagenet_dir" : './datasets/imagenette',
            "teacher_out_channels" : 384,
            "model_size" : EfficientAdModelSize.S,
            "lr" : 0.0001,
            "weight_decay" : 1e-05,
            "padding" : False,
            "pad_maps" : True
        },
        ModelTypeFlag.fastflow_ : {
            "backbone" : "resnet18",
            "pre_trained" : True,
            "flow_steps" : 8,
            "conv3x3_only" : False,
            "hidden_ratio" : 1.0
        },
        ModelTypeFlag.fre_ : {
            "backbone" : "resnet50",
            "layer" : "layer3",
            "pre_trained" : True,
            "pooling_kernel_size" : 2,
            "input_dim" : 65536,
            "latent_dim" : 220

        },
        ModelTypeFlag.ganomaly_ : {
            "batch_size" : 32,
            "n_features" : 64,
            "latent_vec_size" : 100,
            "extra_layers" : 0,
            "add_final_conv_layer" : True,
            "wadv" : 1,
            "wcon" : 50,
            "wenc" : 1,
            "lr" : 0.0002,
            "beta1" : 0.5,
            "beta2" : 0.999
        },
        ModelTypeFlag.padim_ : {
            "backbone" : "resnet18",
            "layers" : ['layer1', 'layer2', 'layer3'],
            "pre_trained" : True,
            "n_features" : 100
        },
        ModelTypeFlag.patchcore_ : {
            "backbone" : "wide_resnet50_2",
            "layers" : ["layer2", "layer3"],
            "pre_trained" : True,
            "coreset_sampling_ratio" : 0.1,
            "num_neighbors" : 9
        },
        ModelTypeFlag.reverse_distillation_ : {
            "backbone" : "wide_resnet50_2",
            "layers" : ["layer1", "layer2", "layer3"],
            "anomaly_map_mode" : AnomalyMapGenerationMode.ADD,
            "pre_trained" : True
        },
        ModelTypeFlag.rkde_ : {
            "roi_stage" : RoiStage.RCNN,
            "roi_score_threshold" : 0.001,
            "min_box_size" : 25,
            "iou_threshold" : 0.3,
            "max_detections_per_image" : 100,
            "n_pca_components" : 16,
            "feature_scaling_method" : FeatureScalingMethod.SCALE,
            "max_training_points" : 40000
        },
        ModelTypeFlag.stfpm_ : {
            "backbone" : "resnet18",
            "layers" : ["layer1", "layer2", "layer3"]
        },
        ModelTypeFlag.uflow_ : {
            "backbone" : "mcait",
            "flow_steps" : 4,
            "affine_clamp" : 2.0,
            "affine_subnet_channels_ratio" : 1.0,
            "permute_soft" : False
        },
        ModelTypeFlag.vlm_ad_ : {},
        ModelTypeFlag.win_clip_ : {
            "class_name" : None,
            "k_shot" : 0,
            "scales" : (2, 3),
            "few_shot_source" : None
        }
    }

    @unique
    class AnomalibLoggerTypeEnum(Enum):
        """
        Enum for different types of logger for anomaly detection models.

        Logger from Anomalib
        COMET : Comet Logger
        MLFLOW : MLFlow Logger
        TENSORBOARD : TensorBoard Logger
        WANDB : Wandb Logger
        """
        comet_ = AnomalibCometLogger
        mlflow_ = AnomalibMLFlowLogger
        tensorboard_ = AnomalibTensorBoardLogger
        wandb_ = AnomalibWandbLogger
        none_ = None

    @unique
    class AnomalibTaskTypeEnum(Enum):   
        """
        Enum for different types of task for anomaly detection models.

        Task from Anomalib
        CLASSIFICATION : Classification Task
        DETECTION : Detection Task
        SEGMENTATION : Segmentation Task
        """
        classification_ = TaskType.CLASSIFICATION
        detection_ = TaskType.DETECTION
        segmentation_ = TaskType.SEGMENTATION

    @unique
    class AnomalibLearningTypeEnum(Enum):
        """
        Enum for different types of learning for anomaly detection models.

        Learning from Anomalib
        ONE_CLASS : One Class Learning
        ZERO_SHOT : Zero Shot Learning
        FEW_SHOT : Few Shot Learning
        """
        one_class_ = LearningType.ONE_CLASS
        zero_shot_ = LearningType.ZERO_SHOT
        few_shot_ = LearningType.FEW_SHOT


    def __init__(self, *, model_type : Optional[ModelTypeFlag] = None, image_metrics : list[str] = ["AUROC"], task : AnomalibTaskTypeEnum = AnomalibTaskTypeEnum.classification_) -> None:
        """
        Initialize the model.

        Args:
            model_type : (Optional[ModelTypeFlag]) : Model for anomaly detection. Default is None.
            image_metrics : (list[str]) : Image metrics for anomaly detection. Default is ["AUROC"].
            task : (AnomalibTaskTypeEnum) : Task for anomaly detection. Default is AnomalibTaskTypeEnum.classification_.
        """
        self.model_ : Optional[AnomalyModule] = None
        self.engine_ : Optional[Engine] = None
        self.model_type_ : Optional[AnomalyModelUnit.ModelTypeFlag] = model_type
        self.image_metrics_ : list[str] = image_metrics
        self.task_ : Optional[AnomalyModelUnit.AnomalibTaskTypeEnum] = task

    def Setter(self, *, model_type : Optional[ModelTypeFlag] = None, image_metrics : list[str] = ["AUROC"], task : AnomalibTaskTypeEnum = AnomalibTaskTypeEnum.classification_) -> None:
        """
        Set the model parameters.

        Args:
            model_type : (Optional[ModelTypeFlag]) : Model for anomaly detection. Default is None.
            image_metrics : (list[str]) : Image metrics for anomaly detection. Default is ["AUROC"].
            task : (AnomalibTaskTypeEnum) : Task for anomaly detection. Default is AnomalibTaskTypeEnum.classification_.

        Example:
        >>> model = AnomalyModelUnit()
        >>> model.Setter(model_type=AnomalyModelType.ganomaly_)
        """
        self.model_type_ = model_type
        self.image_metrics_ = image_metrics
        self.task_ = task

    #@TimeIt
    def Train(self, datamodule : Folder) -> None:
        # This function will implement the training of the model for any model type 
        """
        Train the model using the dataset.

        Args:
            datamodule : Folder : Dataset for training the model.
        
        Example:
        >>> model = AnomalyModelUnit()
        >>> model.Train(datamodule=datamodule)
        """
        assert isinstance(self.model_type_, AnomalyModelUnit.ModelTypeFlag), "Model type is not valid."
        assert isinstance(self.image_metrics_, list), "Image metrics is not valid."
        assert isinstance(self.task_, AnomalyModelUnit.AnomalibTaskTypeEnum), "Task is not valid."

        if not self.ModelValid(model_type=self.model_type_):
            raise ValueError("Model is not implemented.")
        
        self.model_ = self.ModelTypeFlagName[self.model_type_](**self.MODELS_PARAMS_DICT[self.model_type_])

        assert isinstance(self.model_, self.ModelTypeFlagName[self.model_type_]), "Model is not valid."

        early_stopping_callback = EarlyStopping(
            monitor="generator_loss_step" if self.model_type_ in [AnomalyModelUnit.ModelTypeFlag.ganomaly_] else "train_loss_step",
            #monitor="AUROC",
            patience=3,
            mode="min",
            min_delta=0.005,
            verbose=True,
        )

        self.engine_ = Engine(
            normalization=NormalizationMethod.MIN_MAX, # NormalizationMethod.NONE
            threshold="F1AdaptiveThreshold",
            task=self.task_.value,
            image_metrics=self.image_metrics_,
            max_epochs=70,
            callbacks=[] if self.model_type_ in [AnomalyModelUnit.ModelTypeFlag.dfkde_, AnomalyModelUnit.ModelTypeFlag.padim_, AnomalyModelUnit.ModelTypeFlag.patchcore_, AnomalyModelUnit.ModelTypeFlag.cfa_] else [early_stopping_callback],
            #callbacks=[early_stopping_callback],
            accelerator="auto",
            devices="auto",
        )
        self.engine_.fit(model=self.model_, datamodule=datamodule)

    #@TimeIt
    def Evaluate(self, datamodule : Folder):
        """
        Evaluate the model.

        Args:
            datamodule : Folder : Dataset for evaluation.
        
        Example:
        >>> model = AnomalyModelUnit()
        >>> model.Evaluate(datamodule=datamodule)
        """
        assert isinstance(self.model_, AnomalyModule), "Model is not valid."
        assert isinstance(self.engine_, Engine), "Engine is not valid."

        test_result = self.engine_.test(model=self.model_, datamodule=datamodule)
        return test_result

    #@TimeIt
    def Predict(self, data : Folder) -> Any:
        """
        Predict anomalies in the dataset.

        Args:
            data : Folder : Dataset for predicting anomalies.
        
        Returns:
            Any : Predicted anomalies in the dataset.
        
        Example:
        >>> model = AnomalyModelUnit()
        >>> model.Predict(data=test)
        """
        assert isinstance(self.model_, AnomalyModule), "Model is not valid."
        assert isinstance(self.engine_, Engine), "Engine is not valid."
        return self.engine_.predict(model=self.model_, datamodule=data)
    
    def Save(self, path : str) -> None:
        """
        Save the model.

        Args:
            path : str : Path to save the model.

        Example:
        >>> model = AnomalyModelUnit()
        >>> model.Save()
        """
        assert isinstance(self.model_, AnomalyModule), "Model is not valid."
        assert isinstance(self.engine_, Engine), "Engine is not valid."
        self.engine_.export(model=self.model_, export_type=ExportType.TORCH, export_root=path)


    def ModelValid(self, *, model_type : ModelTypeFlag) -> bool:
        """
        Check if the model is valid.

        Args:
            model_type : (ModelTypeFlag) : Model for anomaly detection.

        Returns:
            bool : True if the model is valid, False otherwise.

        Example:
        >>> model = AnomalyModelUnit()
        >>> model.ModelValid(model_type=AnomalyModelType.ganomaly_)
        """
        return self.VALID_MODELS_DICT[model_type]



@Deprecated("This function is deprecated. Use Enum AnomalyModelType instead.")
def GetModel() -> list[str]:
    """
    Deprecated: Returns the list of available anomaly detection models.
    
    Use Enum AnomalyModelType instead.
    """
    return list(get_available_models())
