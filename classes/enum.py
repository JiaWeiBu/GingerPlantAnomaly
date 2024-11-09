# python version : 3.12.6 
from typing import Final
from enum import Enum, unique
from cv2 import IMREAD_COLOR, IMREAD_GRAYSCALE, INTER_NEAREST, INTER_LINEAR, INTER_CUBIC, INTER_LANCZOS4
from cv2 import COLOR_RGB2GRAY, COLOR_GRAY2RGB
from anomalib.models import AiVad, Cfa, Cflow, Csflow, Draem, Dfkde, Dfm, Dsr, EfficientAd, Fastflow, Fre, Ganomaly, Padim, Patchcore, ReverseDistillation, Rkde, Stfpm, Uflow, VlmAd, WinClip

# Enum for color mode
@unique
class ColorMode(Enum):
    """
    Enum for different color modes for image processing.

    RGB : Red-Green-Blue color mode
    GRAYSCALE : Grayscale color mode
    """
    rgb_ = IMREAD_COLOR
    grayscale_ = IMREAD_GRAYSCALE

# Enum for color conversion
@unique
class ColorConversion(Enum):
    """
    Enum for different color conversion methods for image processing.

    RGB2GRAY : Convert RGB to Grayscale
    GRAY2RGB : Convert Grayscale to RGB
    """
    rgb2gray_ = COLOR_RGB2GRAY
    gray2rgb_ = COLOR_GRAY2RGB

@unique
class ImageInterpolation(Enum):
    """
    Enum for different interpolation methods for image resizing.

    NEAREST : Nearest-neighbor interpolation
    LINEAR : Bilinear interpolation
    CUBIC : Bicubic interpolation
    LANCZOS4 : Lanczos interpolation
    """
    nearest_ = INTER_NEAREST
    linear_ = INTER_LINEAR
    cubic_ = INTER_CUBIC
    lanczos4_ = INTER_LANCZOS4

@unique
class PyCaretModelType(Enum):
    """
    Enum for different types of anomaly detection models.

    Model from Pycaret
    ABOD : Angle-base Outlier Detection
    CLUSTER : Clustering-Based Local Outlier
    COF : Connectivity-Based Outlier Factor
    HISTOGRAM : Histogram-based Outlier Detection
    IFOREST : Isolation Forest
    KNN : k-Nearest Neighbors Detector
    LOF : Local Outlier Factor
    SVM : One-class SVM detector
    PCA : Principal Component Analysis
    MCD : Minimum Covariance Determinant
    SOD : Subspace Outlier Detection
    SOS : Stochastic Outlier Selection
    """
    abod_ = "abod"
    cluster_ = "cluster"
    cof_ = "cof"
    histogram_ = "histogram"
    iforest_ = "iforest"
    knn_ = "knn"
    lof_ = "lof"
    svm_ = "svm"
    pca_ = "pca"
    sod_ = "sod"
    sos_ = "sos"
    #mcd_ = "mcd"

# class ModelSource(Enum):
#     """
#     Enum for different sources of anomaly detection models.

#     Model from Pycaret
#     PYCARET : Pycaret library
#     CUSTOM : Custom implementation
#     """
#     pycaret_ = 1
#     custom_ = 2

class PyCaretPlotType(Enum):
    """
    Enum for different types of plots for anomaly detection models.

    Plot from Pycaret
    TSNE : t-Distributed Stochastic Neighbor Embedding
    UMAP : Uniform Manifold Approximation and Projection
    """
    tsne_ = "tsne"
    umap_ = "umap"

@unique
class AnomalyModelType(Enum):
    """
    Enum for different types of anomaly detection models.

    Model from Anomalib
    AI_VAD : AI Video Anomaly Detection
    CFA : Contextual Feature Anomaly
    CFLOW : Contextual Flow Anomaly
    CSFLOW : Contextual Spatial Flow Anomaly
    DRAEM : Deep Recurrent Autoencoder for Extreme Multiclass
    DFKDE : Deep Feature Kernel Density Estimation
    DFM : Deep Feature Matching
    DSR : Deep Spatial Regression
    EFFICIENT_AD : Efficient Anomaly Detection
    FASTFLOW : Fast Flow Anomaly
    FRE : Feature Representation Ensemble
    GANOMALY : GANomaly
    PADIM : Patch-based Anomaly Detection with Image Matching
    PATCHCORE : PatchCore
    REVERSE_DISTILLATION : Reverse Distillation
    RKDE : Robust Kernel Density Estimation
    STFPM : Spatial-Temporal Feature Pyramid Matching
    UFLOW : Unsupervised Flow Anomaly Detection
    VLM_AD : Video-Level Model for Anomaly Detection
    WIN_CLIP : Windowed Clip Anomaly
    """
    ai_vad_ = AiVad
    cfa_ = Cfa
    cflow_ = Cflow
    csflow_ = Csflow
    draem_ = Draem # can or cannot be used
    dfkde_ = Dfkde
    dfm_ = Dfm
    dsr_ = Dsr
    efficient_ad_ = EfficientAd
    fastflow_ = Fastflow
    fre_ = Fre
    ganomaly_ = Ganomaly
    padim_ = Padim
    patchcore_ = Patchcore
    reverse_distillation_ = ReverseDistillation
    rkde_ = Rkde
    stfpm_ = Stfpm
    uflow_ = Uflow
    vlm_ad_ = VlmAd
    win_clip_ = WinClip


VALID_MODELS_DICT: Final[dict[AnomalyModelType, bool]] = {
    AnomalyModelType.ai_vad_ : False,
    AnomalyModelType.cfa_ : False,
    AnomalyModelType.cflow_ : False,
    AnomalyModelType.csflow_ : False,
    AnomalyModelType.draem_ : True,
    AnomalyModelType.dfkde_ : True,
    AnomalyModelType.dfm_ : False,
    AnomalyModelType.dsr_ : False,
    AnomalyModelType.efficient_ad_ : False,
    AnomalyModelType.fastflow_ : True,
    AnomalyModelType.fre_ : False,
    AnomalyModelType.ganomaly_ : True,
    AnomalyModelType.padim_ : True,
    AnomalyModelType.patchcore_ : True,
    AnomalyModelType.reverse_distillation_ : True,
    AnomalyModelType.rkde_ : False,
    AnomalyModelType.stfpm_ : True,
    AnomalyModelType.uflow_ : False,
    AnomalyModelType.vlm_ad_ : False,
    AnomalyModelType.win_clip_ : False
}

from enum import Enum, unique

@unique
class MVTecDatasetType(Enum):
    bottle_ = "bottle"
    cable_ = "cable"
    capsule_ = "capsule"
    carpet_ = "carpet"
    grid_ = "grid"
    hazelnut_ = "hazelnut"
    leather_ = "leather"
    metal_nut_ = "metal_nut"
    pill_ = "pill"
    screw_ = "screw"
    tile_ = "tile"
    toothbrush_ = "toothbrush"
    transistor_ = "transistor"
    wood_ = "wood"
    zipper_ = "zipper"

@unique
class MVTecDatasetTypeAnomaly(Enum):
    broken_large_ = "broken_large" 
    broken_small_ = "broken_small"
    contamination_ = "contamination"
    bent_wire_ = "bent_wire"
    cable_swap_ = "cable_swap"
    combined_ = "combined"
    cut_inner_insulation_ = "cut_inner_insulation"
    cut_outer_insulation_ = "cut_outer_insulation"
    missing_cable_ = "missing_cable"
    missing_wire_ = "missing_wire"
    poke_insulation_ = "poke_insulation"
    crack_ = "crack"
    faulty_imprint_ = "faulty_imprint"
    poke_ = "poke"
    scratch_ = "scratch"
    squeeze_ = "squeeze"
    color_ = "color"
    cut_ = "cut"
    hole_ = "hole"
    metal_contamination_ = "metal_contamination"
    thread_ = "thread"
    bent_ = "bent"
    broken_ = "broken"
    glue_ = "glue"
    print_ = "print"
    fold_ = "fold"
    flip_ = "flip"
    pill_type_ = "pill_type"
    manipulated_front_ = "manipulated_front"
    scratch_head_ = "scratch_head"
    scratch_neck_ = "scratch_neck"
    thread_side_ = "thread_side"
    thread_top_ = "thread_top"
    glue_strip_ = "glue_strip"
    gray_stroke_ = "gray_stroke"
    oil_ = "oil"
    rough_ = "rough"
    defective_ = "defective"
    bent_lead_ = "bent_lead"
    cut_lead_ = "cut_lead"
    damaged_case_ = "damaged_case"
    misplaced_ = "misplaced"
    liquid_ = "liquid"
    broken_teeth_ = "broken_teeth"
    fabric_border_ = "fabric_border"
    fabric_interior_ = "fabric_interior"
    split_teeth_ = "split_teeth"
    squeezed_teeth_ = "squeezed_teeth"

# hash table for MVTec dataset
MVTecDataset : dict[MVTecDatasetType, list[MVTecDatasetTypeAnomaly]] = {
    MVTecDatasetType.bottle_ : [
        MVTecDatasetTypeAnomaly.broken_large_, 
        MVTecDatasetTypeAnomaly.broken_small_, 
        MVTecDatasetTypeAnomaly.contamination_
        ],

    MVTecDatasetType.cable_ : [ 
        MVTecDatasetTypeAnomaly.bent_wire_,
        MVTecDatasetTypeAnomaly.cable_swap_, 
        MVTecDatasetTypeAnomaly.combined_, 
        MVTecDatasetTypeAnomaly.cut_inner_insulation_, 
        MVTecDatasetTypeAnomaly.cut_outer_insulation_, 
        MVTecDatasetTypeAnomaly.missing_cable_, 
        MVTecDatasetTypeAnomaly.missing_wire_, 
        MVTecDatasetTypeAnomaly.poke_insulation_
        ],

    MVTecDatasetType.capsule_ : [
        MVTecDatasetTypeAnomaly.crack_, 
        MVTecDatasetTypeAnomaly.faulty_imprint_, 
        MVTecDatasetTypeAnomaly.poke_, 
        MVTecDatasetTypeAnomaly.scratch_, 
        MVTecDatasetTypeAnomaly.squeeze_
        ],

    MVTecDatasetType.carpet_ : [
        MVTecDatasetTypeAnomaly.color_, 
        MVTecDatasetTypeAnomaly.cut_, 
        MVTecDatasetTypeAnomaly.hole_, 
        MVTecDatasetTypeAnomaly.metal_contamination_, 
        MVTecDatasetTypeAnomaly.thread_
        ],

    MVTecDatasetType.grid_ : [
        MVTecDatasetTypeAnomaly.bent_, 
        MVTecDatasetTypeAnomaly.broken_, 
        MVTecDatasetTypeAnomaly.glue_, 
        MVTecDatasetTypeAnomaly.metal_contamination_, 
        MVTecDatasetTypeAnomaly.thread_
        ],

    MVTecDatasetType.hazelnut_ : [
        MVTecDatasetTypeAnomaly.crack_, 
        MVTecDatasetTypeAnomaly.cut_, 
        MVTecDatasetTypeAnomaly.hole_, 
        MVTecDatasetTypeAnomaly.print_
        ],

    MVTecDatasetType.leather_ : [
        MVTecDatasetTypeAnomaly.color_,
        MVTecDatasetTypeAnomaly.cut_, 
        MVTecDatasetTypeAnomaly.fold_, 
        MVTecDatasetTypeAnomaly.glue_,
        MVTecDatasetTypeAnomaly.poke_,
        ],

    MVTecDatasetType.metal_nut_ : [
        MVTecDatasetTypeAnomaly.bent_, 
        MVTecDatasetTypeAnomaly.color_, 
        MVTecDatasetTypeAnomaly.flip_,
        MVTecDatasetTypeAnomaly.scratch_,
        ],

    MVTecDatasetType.pill_ : [
        MVTecDatasetTypeAnomaly.color_,
        MVTecDatasetTypeAnomaly.combined_,
        MVTecDatasetTypeAnomaly.contamination_,
        MVTecDatasetTypeAnomaly.crack_,
        MVTecDatasetTypeAnomaly.faulty_imprint_,
        MVTecDatasetTypeAnomaly.pill_type_,
        MVTecDatasetTypeAnomaly.scratch_,
        ],

    MVTecDatasetType.screw_ : [
        MVTecDatasetTypeAnomaly.manipulated_front_,
        MVTecDatasetTypeAnomaly.scratch_head_,
        MVTecDatasetTypeAnomaly.scratch_neck_,
        MVTecDatasetTypeAnomaly.thread_side_,
        MVTecDatasetTypeAnomaly.thread_top_,
        ],

    MVTecDatasetType.tile_ : [
        MVTecDatasetTypeAnomaly.crack_,
        MVTecDatasetTypeAnomaly.glue_strip_,
        MVTecDatasetTypeAnomaly.gray_stroke_,
        MVTecDatasetTypeAnomaly.oil_,
        MVTecDatasetTypeAnomaly.rough_,
        ],

    MVTecDatasetType.toothbrush_ : [ 
        MVTecDatasetTypeAnomaly.defective_,
        ],

    MVTecDatasetType.transistor_ : [
        MVTecDatasetTypeAnomaly.bent_lead_,
        MVTecDatasetTypeAnomaly.cut_lead_,
        MVTecDatasetTypeAnomaly.damaged_case_,
        MVTecDatasetTypeAnomaly.misplaced_,
        ],

    MVTecDatasetType.wood_ : [
        MVTecDatasetTypeAnomaly.color_,
        MVTecDatasetTypeAnomaly.combined_,
        MVTecDatasetTypeAnomaly.hole_,
        MVTecDatasetTypeAnomaly.liquid_,
        MVTecDatasetTypeAnomaly.scratch_,
        ],

    MVTecDatasetType.zipper_ : [
        MVTecDatasetTypeAnomaly.broken_teeth_,
        MVTecDatasetTypeAnomaly.combined_,
        MVTecDatasetTypeAnomaly.fabric_border_,
        MVTecDatasetTypeAnomaly.fabric_interior_,
        MVTecDatasetTypeAnomaly.rough_,
        MVTecDatasetTypeAnomaly.split_teeth_,
        MVTecDatasetTypeAnomaly.squeezed_teeth_,
        ]
}