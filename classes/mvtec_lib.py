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