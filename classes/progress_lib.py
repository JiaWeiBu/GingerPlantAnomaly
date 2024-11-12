# i want to keep track on the progress of he model and dataset used based on the enum
# i want the program abl eto read
from typing import Optional
from classes.anomalib_lib import AnomalyModelUnit
from classes.dataset_lib import DatasetUnit

class ProgressUnit:
    """
    ProgressUnit class is used to keep track of the progress of the model and dataset used in the Anomalib project

    Attributes:
        dataset_type_progress_ : Optional[DatasetUnit.MVTecDatasetTypeEnum] : The dataset type that the program is currently on
        model_type_progress_ : Optional[AnomalyModelUnit.AnomalyModelTypeEnum] : The model type that the program is currently on
        file_path_ : str : The file path to the progress file
        dataset_dict_ : dict[str, DatasetUnit.MVTecDatasetTypeEnum] : The dictionary of the dataset type enum
        model_dict_ : dict[str, AnomalyModelUnit.AnomalyModelTypeEnum] : The dictionary of the model type enum
        progression_matrix_ : dict[DatasetUnit.MVTecDatasetTypeEnum, dict[AnomalyModelUnit.AnomalyModelTypeEnum, bool]] : The matrix of the progress of the program
    
    Methods:
        write_progress : None : Writes the current progress to the progress file
        update_progress : None : Updates the current progress of the program
        read_progress : None : Reads the progress from the progress file
        matrix_gen : None : Generates the matrix of the progress
        new_progress : None : Resets the progress of the program
    
    Example:
    >>> progress_unit : ProgressUnit = ProgressUnit()
    >>> progress_unit.read_progress()
    >>> progress_unit.update_progress(DatasetUnit.MVTecDatasetTypeEnum.bottle_, AnomalyModelUnit.AnomalyModelTypeEnum.padim_)
    >>> progress_unit.write_progress()
    """

    def __init__(self, dataset_type_progress : Optional[DatasetUnit.MVTecDatasetTypeEnum] = None, model_type_progress : Optional[AnomalyModelUnit.AnomalyModelTypeEnum] = None):
        self.dataset_type_progress_ : Optional[DatasetUnit.MVTecDatasetTypeEnum] = dataset_type_progress
        self.model_type_progress_ : Optional[AnomalyModelUnit.AnomalyModelTypeEnum] = model_type_progress
        self.file_path_ : str = "progress.txt"
        self.dataset_dict_ : dict[str, DatasetUnit.MVTecDatasetTypeEnum] = {
            f"{DatasetUnit.MVTecDatasetTypeEnum.bottle_.value}" : DatasetUnit.MVTecDatasetTypeEnum.bottle_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.cable_.value}" : DatasetUnit.MVTecDatasetTypeEnum.cable_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.capsule_.value}" : DatasetUnit.MVTecDatasetTypeEnum.capsule_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.carpet_.value}" : DatasetUnit.MVTecDatasetTypeEnum.carpet_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.grid_.value}" : DatasetUnit.MVTecDatasetTypeEnum.grid_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.hazelnut_.value}" : DatasetUnit.MVTecDatasetTypeEnum.hazelnut_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.leather_.value}" : DatasetUnit.MVTecDatasetTypeEnum.leather_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.metal_nut_.value}" : DatasetUnit.MVTecDatasetTypeEnum.metal_nut_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.pill_.value}" : DatasetUnit.MVTecDatasetTypeEnum.pill_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.screw_.value}" : DatasetUnit.MVTecDatasetTypeEnum.screw_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.tile_.value}" : DatasetUnit.MVTecDatasetTypeEnum.tile_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.toothbrush_.value}" : DatasetUnit.MVTecDatasetTypeEnum.toothbrush_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.transistor_.value}" : DatasetUnit.MVTecDatasetTypeEnum.transistor_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.wood_.value}" : DatasetUnit.MVTecDatasetTypeEnum.wood_,
            f"{DatasetUnit.MVTecDatasetTypeEnum.zipper_.value}" : DatasetUnit.MVTecDatasetTypeEnum.zipper_,
        }
        self.model_dict_ : dict[str, AnomalyModelUnit.AnomalyModelTypeEnum] ={
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.ai_vad_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.ai_vad_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.cfa_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.cfa_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.cflow_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.cflow_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.csflow_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.csflow_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.draem_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.draem_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.dfkde_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.dfkde_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.dfm_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.dfm_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.dsr_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.dsr_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.efficient_ad_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.efficient_ad_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.fastflow_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.fastflow_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.fre_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.fre_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.ganomaly_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.ganomaly_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.padim_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.padim_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.patchcore_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.patchcore_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.reverse_distillation_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.reverse_distillation_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.rkde_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.rkde_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.stfpm_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.stfpm_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.uflow_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.uflow_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.vlm_ad_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.vlm_ad_,
            f"{AnomalyModelUnit.AnomalyModelTypeEnum.win_clip_.name}" : AnomalyModelUnit.AnomalyModelTypeEnum.win_clip_,
        }
        self.progression_matrix_ : dict[DatasetUnit.MVTecDatasetTypeEnum, dict[AnomalyModelUnit.AnomalyModelTypeEnum, bool]] = {}

    def write_progress(self) -> None:
        """
        Writes the current progress to the progress file

        Example:
        >>> progress_unit : ProgressUnit = ProgressUnit()
        >>> progress_unit.write_progress()
        """
        assert isinstance(self.dataset_type_progress_, DatasetUnit.MVTecDatasetTypeEnum)
        assert isinstance(self.model_type_progress_, AnomalyModelUnit.AnomalyModelTypeEnum)
        with open(self.file_path_, "w", encoding="utf-8") as f:
            f.write(f"{self.dataset_type_progress_.value}\n")
            f.write(f"{self.model_type_progress_.name}\n")

    def update_progress(self, dataset_type : DatasetUnit.MVTecDatasetTypeEnum, model_type : AnomalyModelUnit.AnomalyModelTypeEnum) -> None:
        """
        Updates the current progress of the program

        Args:
            dataset_type : DatasetUnit.MVTecDatasetTypeEnum : The dataset type to update the progress to
            model_type : AnomalyModelUnit.AnomalyModelTypeEnum : The model type to update the progress to
        
        Example:
        >>> progress_unit : ProgressUnit = ProgressUnit()
        >>> progress_unit.update_progress(DatasetUnit.MVTecDatasetTypeEnum.bottle_, AnomalyModelUnit.AnomalyModelTypeEnum.padim_)
        """
        self.dataset_type_progress_ = dataset_type
        self.model_type_progress_ = model_type
        self.write_progress()
    
    def read_progress(self) -> None:
        """
        Reads the progress from the progress file

        Example:
        >>> progress_unit : ProgressUnit = ProgressUnit()
        >>> progress_unit.read_progress()
        """
        with open(self.file_path_, "r", encoding="utf-8") as f:
            dataset_type = f.readline().strip()
            model_type = f.readline().strip()
            self.dataset_type_progress_ = self.dataset_dict_[dataset_type]
            self.model_type_progress_ = self.model_dict_[model_type]
            self.matrix_gen()

    def matrix_gen(self) -> None:
        """
        Generates the matrix of the progress

        Example:
        >>> progress_unit : ProgressUnit = ProgressUnit()
        >>> progress_unit.matrix_gen()
        """
        run : bool = True
        for dataset_type in DatasetUnit.MVTecDatasetTypeEnum:
            self.progression_matrix_[dataset_type] = {}
            for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
                self.progression_matrix_[dataset_type][model_type] = run
                if dataset_type == self.dataset_type_progress_ and model_type == self.model_type_progress_:    
                    run = False

    def new_progress(self) -> None:
        """
        Resets the progress of the program

        Example:
        >>> progress_unit : ProgressUnit = ProgressUnit()
        >>> progress_unit.new_progress()
        """
        with open(self.file_path_, "w", encoding="utf-8") as f:
            ...
        for dataset_type in DatasetUnit.MVTecDatasetTypeEnum:
            self.progression_matrix_[dataset_type] = {}
            for model_type in AnomalyModelUnit.AnomalyModelTypeEnum:
                self.progression_matrix_[dataset_type][model_type] = False
            
            
            

    