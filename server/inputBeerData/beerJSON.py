from typing import Optional
from pydantic import BaseModel, validator
from fastapi import status

INTENSITY_TYPES = ["baja", "media", "alta", "*"]
COLOR_TYPES = ["palido", "ambar", "oscuro", "*"]
BITTERNESS_TYPES = ["bajo", "medio", "alto", "*"]
HOP_TYPES = ["viejo mundo", "nuevo mundo", "*"]
FERMENTATION_TYPES = ["baja", "media", "alta", "*"]
YEAST_TYPES = ["lager", "ale", "*"]


class ValidationError(Exception):
    def __init__(self, message):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = message


class InputBody(BaseModel):
    intensity: Optional[str] = "*"
    color: Optional[str] = "*"
    bitterness: Optional[str] = "*"
    hop: Optional[str] = "*"
    fermentation: Optional[str] = "*"
    yeast: Optional[str] = "*"

    @validator("intensity")
    def validateIntensity(cls, intensity):
        intensity = intensity.lower()
        if intensity not in INTENSITY_TYPES:
            raise ValidationError(
                getErrorMessage("intensity", INTENSITY_TYPES, intensity)
            )

        return intensity

    @validator("color")
    def validateColor(cls, color):
        color = color.lower()
        if color not in COLOR_TYPES:
            raise ValidationError(getErrorMessage("color", COLOR_TYPES, color))

        return color

    @validator("bitterness")
    def validateBitterness(cls, bitterness):
        bitterness = bitterness.lower()
        if bitterness not in BITTERNESS_TYPES:
            raise ValidationError(
                getErrorMessage("bitterness", BITTERNESS_TYPES, bitterness)
            )

        return bitterness

    @validator("hop")
    def validateHop(cls, hop):
        hop = hop.lower()
        if hop not in HOP_TYPES:
            raise ValidationError(getErrorMessage("hop", HOP_TYPES, hop))

        return hop

    @validator("fermentation")
    def validateFermentation(cls, fermentation):
        fermentation = fermentation.lower()
        if fermentation not in FERMENTATION_TYPES:
            raise ValidationError(
                getErrorMessage("fermentation", FERMENTATION_TYPES, fermentation)
            )

        return fermentation

    @validator("yeast")
    def validateYeast(cls, yeast):
        yeast = yeast.lower()
        if yeast not in YEAST_TYPES:
            raise ValidationError(getErrorMessage("yeast", YEAST_TYPES, yeast))

        return yeast


def getErrorMessage(attribute, expectedValues, actualValue):
    return f"invalid {attribute} type. Must be {expectedValues}, got '{actualValue}'"
