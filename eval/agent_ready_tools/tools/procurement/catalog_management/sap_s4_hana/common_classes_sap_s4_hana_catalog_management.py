from enum import StrEnum


class S4HANAIndustrySector(StrEnum):
    """The industry sector of the material."""

    PLANT_ENGINEERING_AND_CONSTRUCTION = "A"
    CHEMICAL = "C"
    MECHANICAL_ENGINEERING = "M"
    PHARMACEUTICAL = "P"


class S4HANABaseUnit(StrEnum):
    """The base unit of measure for material."""

    BAG = "BAG"
    BOTTLE = "BT"
    CARTON = "CAR"
    CRATE = "CR"
    CASE = "CV"
    DRUM = "DR"
    EACH = "EA"
    KILOGRAM = "KG"
    PACK = "PAC"
    PALLET = "PAL"
    PIECE = "PC"
