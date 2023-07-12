from pydantic import BaseModel, field_validator
from fastapi import HTTPException


class Point(BaseModel):
    lat: float
    lon: float

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    @field_validator("lat")
    def check_lat_value(cls, value):
        if -90 <= value <= 90:
            return value
        raise HTTPException(status_code=422, detail="Latitude in range from -90 to 90.")

    @field_validator("lon")
    def check_lon_value(cls, value):
        if -180 <= value <= 180:
            return value
        raise HTTPException(status_code=422, detail="Longitude in range from -180 to 180.")
