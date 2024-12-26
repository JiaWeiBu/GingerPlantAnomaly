from enum import Enum, unique

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

# import all the torch model for all anomalib model
from anomalib.models.video.ai_vad.torch_model import AiVadModel
from anomalib.models.image.cfa.torch_model import CfaModel
from anomalib.models.image.cflow.torch_model import CflowModel
from anomalib.models.image.csflow.torch_model import CsFlowModel
from anomalib.models.image.draem.torch_model import DraemModel
from anomalib.models.image.dfkde.torch_model import DfkdeModel
from anomalib.models.image.dfm.torch_model import DFMModel
from anomalib.models.image.dsr.torch_model import DsrModel
from anomalib.models.image.efficient_ad.torch_model import EfficientAdModel
from anomalib.models.image.fastflow.torch_model import FastflowModel
from anomalib.models.image.fre.torch_model import FREModel
from anomalib.models.image.ganomaly.torch_model import GanomalyModel
from anomalib.models.image.padim.torch_model import PadimModel
from anomalib.models.image.patchcore.torch_model import PatchcoreModel
from anomalib.models.image.reverse_distillation.torch_model import ReverseDistillationModel
from anomalib.models.image.rkde.torch_model import RkdeModel
from anomalib.models.image.stfpm.torch_model import STFPMModel
from anomalib.models.image.uflow.torch_model import UflowModel
#from anomalib.models.image.vlm_ad.torch_model import VlmAdModel
from anomalib.models.image.winclip.torch_model import WinClipModel


from lightning.pytorch.callbacks.early_stopping import EarlyStopping

from classes.util_lib import Deprecated, TimeIt

class AnomalyModelUnit: 
    """
    Class for anomaly detection model unit.
    Each model will be trained using the dataset and the model will be saved.

    Enum:
        AnomalyModelTypeEnum : Enum for different types of anomaly detection models.
        AnomalibLoggerTypeEnum : Enum for different types of logger for anomaly detection models.
        AnomalibTaskTypeEnum : Enum for different types of task for anomaly detection models.
        AnomalibLearningTypeEnum : Enum for different types of learning for anomaly detection models
    
    Dictionary:
        VALID_MODELS_DICT : Dict[AnomalyModelTypeEnum, bool] : Dictionary for valid models.
        MODELS_PARAMS_DICT : Dict[AnomalyModelTypeEnum, Dict[str, Any]] : Dictionary for model parameters.

    Attributes:
        model_ : Optional[AnomalyModule] : Internal Anomalib model.
        engine_ : Optional[Engine] : Internal Anomalib engine.
        model_type_ : Optional[AnomalyModelTypeEnum] : Model for anomaly detection.
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
    class AnomalyModelTypeEnum(Enum):
        """
        Enum for different types of anomaly detection models.

        Model from Anomalib
        AI_VAD : Accurate and Interpretable Video Anomaly Detection
        CFA : Coupled-hypersphere-based Feature Adaptation
        CFLOW : Conditional Normalizing Flows
        CSFLOW : Cross-Scale-Flows
        DRÆM : Discriminatively Trained Reconstruction Anomaly Embedding Model
        DFKDE : Deep Feature Kernel Density Estimation
        DFM : Deep Feature Modelling
        DSR : Dual Subspace Re-Projections
        EFFICIENT_AD : Efficient Anomaly Detection
        FASTFLOW : Fast Flow Anomaly
        FRE : Feature Reconstruction Error
        GANOMALY :  Generative Adversarial Networks for Anomaly Detection
        PADIM : Patch Distribution Modeling
        PATCHCORE : PatchCore
        REVERSE_DISTILLATION : Reverse Distillation
        RKDE : Region-Based Kernel Density Estimation
        STFPM : Student-Teacher Feature Pyramid Matching
        UFLOW :  U-shaped Normalizing Flow
        VLM_AD : Video-Level Model for Anomaly Detection
        WIN_CLIP : Windowed-Based Contrastive Language-Image Pre-training
        """
        # ai_vad_ = AiVad
        # cfa_ = Cfa
        # cflow_ = Cflow
        # csflow_ = Csflow
        # draem_ = Draem # can or cannot be used
        # dfkde_ = Dfkde
        # dfm_ = Dfm
        # dsr_ = Dsr
        # efficient_ad_ = EfficientAd
        # fastflow_ = Fastflow
        # fre_ = Fre
        # ganomaly_ = Ganomaly
        # padim_ = Padim
        # patchcore_ = Patchcore
        # reverse_distillation_ = ReverseDistillation
        # rkde_ = Rkde
        # stfpm_ = Stfpm
        # uflow_ = Uflow
        # vlm_ad_ = VlmAd
        # win_clip_ = WinClip

        padim_ = Padim
        dfkde_ = Dfkde
        patchcore_ = Patchcore
        ganomaly_ = Ganomaly
        draem_ = Draem
        reverse_distillation_ = ReverseDistillation
        stfpm_ = Stfpm
        fastflow_ = Fastflow
        ai_vad_ = AiVad
        cfa_ = Cfa
        cflow_ = Cflow
        csflow_ = Csflow
        dsr_ = Dsr
        dfm_ = Dfm
        fre_ = Fre
        efficient_ad_ = EfficientAd
        uflow_ = Uflow
        rkde_ = Rkde
        win_clip_ = WinClip
        vlm_ad_ = VlmAd


    # @unique
    # class AnomalyModelPyTorchModelTypeEnum(Enum):
    #     """
    #     Enum for different types of anomaly detection models.

    #     Model from PyTorch
    #     AI_VAD : AI Video Anomaly Detection
    #     CFA : Contextual Feature Anomaly
    #     CFLOW : Contextual Flow Anomaly
    #     CSFLOW : Contextual Spatial Flow Anomaly
    #     DRAEM : Deep Recurrent Autoencoder for Extreme Multiclass
    #     DFKDE : Deep Feature Kernel Density Estimation
    #     DFM : Deep Feature Matching
    #     DSR : Deep Spatial Regression
    #     EFFICIENT_AD : Efficient Anomaly Detection
    #     FASTFLOW : Fast Flow Anomaly
    #     FRE : Feature Representation Ensemble
    #     GANOMALY : GANomaly
    #     PADIM : Patch-based Anomaly Detection with Image Matching
    #     PATCHCORE : PatchCore
    #     REVERSE_DISTILLATION : Reverse Distillation
    #     RKDE : Robust Kernel Density Estimation
    #     STFPM : Spatial-Temporal Feature Pyramid Matching
    #     UFLOW : Unsupervised Flow Anomaly Detection
    #     VLM_AD : Video-Level Model for Anomaly Detection
    #     WIN_CLIP : Windowed Clip Anomaly
    #     """
    #     ai_vad_ = AiVadModel
    #     cfa_ = CfaModel
    #     cflow_ = CflowModel
    #     csflow_ = CsflowModel
    #     draem_ = DraemModel
    #     dfkde_ = DfkdeModel
    #     dfm_ = DfmModel
    #     dsr_ = DsrModel
    #     efficient_ad_ = EfficientAdModel
    #     fastflow_ = FastflowModel
    #     fre_ = FreModel
    #     ganomaly_ = GanomalyModel
    #     padim_ = PadimModel
    #     patchcore_ = PatchcoreModel
    #     reverse_distillation_ = ReverseDistillationModel
    #     rkde_ = RkdeModel
    #     stfpm_ = StfpmModel
    #     uflow_ = UflowModel
    #     vlm_ad_ = VlmAdModel
    #     win_clip_ = WinClipModel

    PyTorchModelDict : Final[dict[AnomalyModelTypeEnum, Any]] = {
        AnomalyModelTypeEnum.ai_vad_ : AiVadModel,
        AnomalyModelTypeEnum.cfa_ : CfaModel,
        AnomalyModelTypeEnum.cflow_ : CflowModel,
        AnomalyModelTypeEnum.csflow_ : CsFlowModel,
        AnomalyModelTypeEnum.draem_ : DraemModel,
        AnomalyModelTypeEnum.dfkde_ : DfkdeModel,
        AnomalyModelTypeEnum.dfm_ : DFMModel,
        AnomalyModelTypeEnum.dsr_ : DsrModel,
        AnomalyModelTypeEnum.efficient_ad_ : EfficientAdModel,
        AnomalyModelTypeEnum.fastflow_ : FastflowModel,
        AnomalyModelTypeEnum.fre_ : FREModel,
        AnomalyModelTypeEnum.ganomaly_ : GanomalyModel,
        AnomalyModelTypeEnum.padim_ : PadimModel,
        AnomalyModelTypeEnum.patchcore_ : PatchcoreModel,
        AnomalyModelTypeEnum.reverse_distillation_ : ReverseDistillationModel,
        AnomalyModelTypeEnum.rkde_ : RkdeModel,
        AnomalyModelTypeEnum.stfpm_ : STFPMModel,
        AnomalyModelTypeEnum.uflow_ : UflowModel,
        #AnomalyModelTypeEnum.vlm_ad_ : VlmAdModel,
        AnomalyModelTypeEnum.win_clip_ : WinClipModel
    }

    VALID_MODELS_DICT: Final[dict[AnomalyModelTypeEnum, bool]] = {
        AnomalyModelTypeEnum.ai_vad_ : False,
        AnomalyModelTypeEnum.cfa_ : False,
        AnomalyModelTypeEnum.cflow_ : False,
        AnomalyModelTypeEnum.csflow_ : False,
        AnomalyModelTypeEnum.draem_ : True,
        AnomalyModelTypeEnum.dfkde_ : True,
        AnomalyModelTypeEnum.dfm_ : False,
        AnomalyModelTypeEnum.dsr_ : False,
        AnomalyModelTypeEnum.efficient_ad_ : False,
        AnomalyModelTypeEnum.fastflow_ : True,
        AnomalyModelTypeEnum.fre_ : False,
        AnomalyModelTypeEnum.ganomaly_ : True,
        AnomalyModelTypeEnum.padim_ : True,
        AnomalyModelTypeEnum.patchcore_ : True,
        AnomalyModelTypeEnum.reverse_distillation_ : True,
        AnomalyModelTypeEnum.rkde_ : False,
        AnomalyModelTypeEnum.stfpm_ : True,
        AnomalyModelTypeEnum.uflow_ : False,
        AnomalyModelTypeEnum.vlm_ad_ : False,
        AnomalyModelTypeEnum.win_clip_ : False

        # # set all models to True
        # AnomalyModelTypeEnum.ai_vad_ : False,
        # AnomalyModelTypeEnum.cfa_ : True,
        # AnomalyModelTypeEnum.cflow_ : True,
        # AnomalyModelTypeEnum.csflow_ : True,
        # AnomalyModelTypeEnum.draem_ : True,
        # AnomalyModelTypeEnum.dfkde_ : True,
        # AnomalyModelTypeEnum.dfm_ : True,
        # AnomalyModelTypeEnum.dsr_ : True,
        # AnomalyModelTypeEnum.efficient_ad_ : True,
        # AnomalyModelTypeEnum.fastflow_ : True,
        # AnomalyModelTypeEnum.fre_ : True,
        # AnomalyModelTypeEnum.ganomaly_ : True,
        # AnomalyModelTypeEnum.padim_ : True,
        # AnomalyModelTypeEnum.patchcore_ : True,
        # AnomalyModelTypeEnum.reverse_distillation_ : True,
        # AnomalyModelTypeEnum.rkde_ : True,
        # AnomalyModelTypeEnum.stfpm_ : True,
        # AnomalyModelTypeEnum.uflow_ : True,
        # AnomalyModelTypeEnum.vlm_ad_ : False,
        # AnomalyModelTypeEnum.win_clip_ : True            
    }

    MODELS_PARAMS_DICT: Final[dict[AnomalyModelTypeEnum, dict[str, Any]]] = {
        AnomalyModelTypeEnum.ai_vad_ : { 
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
        AnomalyModelTypeEnum.cfa_ : {
            "backbone" : "wide_resnet50_2",
            "gamma_c" : 1,
            "gamma_d" : 1,
            "num_nearest_neighbors" : 3,
            "num_hard_negative_features" : 3,
            "radius" : 1e-05
        },
        AnomalyModelTypeEnum.cflow_ : {
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
        AnomalyModelTypeEnum.csflow_ : {
            "cross_conv_hidden_channels" : 1024,
            "n_coupling_blocks" : 4,
            "clamp" : 3,
            "num_channels" : 3
        },
        AnomalyModelTypeEnum.draem_ : {
            "enable_sspcab" : False,
            "sspcab_lambda" : 0.1,
            "anomaly_source_path" : None,
            "beta" : (0.1, 1.0)
        },
        AnomalyModelTypeEnum.dfkde_ : {
            "backbone" : "resnet18",
            "layers" : ('layer4',),
            "pre_trained" : True,
            "n_pca_components" : 16,
            "feature_scaling_method" : FeatureScalingMethod.SCALE,
            "max_training_points" : 40000
        },
        AnomalyModelTypeEnum.dfm_ : {
            "backbone" : "resnet50",
            "layer" : "layer3",
            "pre_trained" : True,
            "pooling_kernel_size" : 4,
            "pca_level" : 0.97,
            "score_type" : "fre"
        },
        AnomalyModelTypeEnum.dsr_ : {
            "latent_anomaly_strength" : 0.2,
            "embedding_dim" : 128,
            "num_embeddings" : 4096,
            "num_hiddens" : 128,
            "num_residual_layers" : 2,
            "num_residual_hiddens" : 64
        },
        AnomalyModelTypeEnum.efficient_ad_ : {#imagenet_dir='./datasets/imagenette', teacher_out_channels=384, model_size=EfficientAdModelSize.S, lr=0.0001, weight_decay=1e-05, padding=False, pad_maps=True
            "imagenet_dir" : './datasets/imagenette',
            "teacher_out_channels" : 384,
            "model_size" : EfficientAdModelSize.S,
            "lr" : 0.0001,
            "weight_decay" : 1e-05,
            "padding" : False,
            "pad_maps" : True
        },
        AnomalyModelTypeEnum.fastflow_ : {
            "backbone" : "resnet18",
            "pre_trained" : True,
            "flow_steps" : 8,
            "conv3x3_only" : False,
            "hidden_ratio" : 1.0
        },
        AnomalyModelTypeEnum.fre_ : {
            "backbone" : "resnet50",
            "layer" : "layer3",
            "pre_trained" : True,
            "pooling_kernel_size" : 2,
            "input_dim" : 65536,
            "latent_dim" : 220

        },
        AnomalyModelTypeEnum.ganomaly_ : {
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
        AnomalyModelTypeEnum.padim_ : {
            "backbone" : "resnet18",
            "layers" : ['layer1', 'layer2', 'layer3'],
            "pre_trained" : True,
            "n_features" : 100
        },
        AnomalyModelTypeEnum.patchcore_ : {
            "backbone" : "wide_resnet50_2",
            "layers" : ["layer2", "layer3"],
            "pre_trained" : True,
            "coreset_sampling_ratio" : 0.1,
            "num_neighbors" : 9
        },
        AnomalyModelTypeEnum.reverse_distillation_ : {
            "backbone" : "wide_resnet50_2",
            "layers" : ["layer1", "layer2", "layer3"],
            "anomaly_map_mode" : AnomalyMapGenerationMode.ADD,
            "pre_trained" : True
        },
        AnomalyModelTypeEnum.rkde_ : {
            "roi_stage" : RoiStage.RCNN,
            "roi_score_threshold" : 0.001,
            "min_box_size" : 25,
            "iou_threshold" : 0.3,
            "max_detections_per_image" : 100,
            "n_pca_components" : 16,
            "feature_scaling_method" : FeatureScalingMethod.SCALE,
            "max_training_points" : 40000
        },
        AnomalyModelTypeEnum.stfpm_ : {
            "backbone" : "resnet18",
            "layers" : ["layer1", "layer2", "layer3"]
        },
        AnomalyModelTypeEnum.uflow_ : {
            "backbone" : "mcait",
            "flow_steps" : 4,
            "affine_clamp" : 2.0,
            "affine_subnet_channels_ratio" : 1.0,
            "permute_soft" : False
        },
        AnomalyModelTypeEnum.vlm_ad_ : {},
        AnomalyModelTypeEnum.win_clip_ : {
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


    def __init__(self, *, model_type : Optional[AnomalyModelTypeEnum] = None, image_metrics : list[str] = ["AUROC"], task : AnomalibTaskTypeEnum = AnomalibTaskTypeEnum.classification_) -> None:
        """
        Initialize the model.

        Args:
            model_type : (Optional[AnomalyModelTypeEnum]) : Model for anomaly detection. Default is None.
            image_metrics : (list[str]) : Image metrics for anomaly detection. Default is ["AUROC"].
            task : (AnomalibTaskTypeEnum) : Task for anomaly detection. Default is AnomalibTaskTypeEnum.classification_.
        """
        self.model_ : Optional[AnomalyModule] = None
        self.engine_ : Optional[Engine] = None
        self.model_type_ : Optional[AnomalyModelUnit.AnomalyModelTypeEnum] = model_type
        self.image_metrics_ : list[str] = image_metrics
        self.task_ : Optional[AnomalyModelUnit.AnomalibTaskTypeEnum] = task

    def Setter(self, *, model_type : Optional[AnomalyModelTypeEnum] = None, image_metrics : list[str] = ["AUROC"], task : AnomalibTaskTypeEnum = AnomalibTaskTypeEnum.classification_) -> None:
        """
        Set the model parameters.

        Args:
            model_type : (Optional[AnomalyModelTypeEnum]) : Model for anomaly detection. Default is None.
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
        assert isinstance(self.model_type_, AnomalyModelUnit.AnomalyModelTypeEnum), "Model type is not valid."
        assert isinstance(self.image_metrics_, list), "Image metrics is not valid."
        assert isinstance(self.task_, AnomalyModelUnit.AnomalibTaskTypeEnum), "Task is not valid."

        if not self.ModelValid(model_type=self.model_type_):
            raise ValueError("Model is not implemented.")
        
        self.model_ = self.model_type_.value(**self.MODELS_PARAMS_DICT[self.model_type_])

        assert isinstance(self.model_, self.model_type_.value), "Model is not valid."

        early_stopping_callback = EarlyStopping(
            monitor="generator_loss_step" if self.model_type_ in [AnomalyModelUnit.AnomalyModelTypeEnum.ganomaly_] else "train_loss_step",
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
            callbacks=[] if self.model_type_ in [AnomalyModelUnit.AnomalyModelTypeEnum.dfkde_, AnomalyModelUnit.AnomalyModelTypeEnum.padim_, AnomalyModelUnit.AnomalyModelTypeEnum.patchcore_, AnomalyModelUnit.AnomalyModelTypeEnum.cfa_] else [early_stopping_callback],
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


    def ModelValid(self, *, model_type : AnomalyModelTypeEnum) -> bool:
        """
        Check if the model is valid.

        Args:
            model_type : (AnomalyModelTypeEnum) : Model for anomaly detection.

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
