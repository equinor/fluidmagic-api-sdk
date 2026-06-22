"""Collection of facility entities used in the api."""

from pydantic import BaseModel, ConfigDict, Field


class FacilityModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_name: str = Field(..., description="Facility name.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "facility_1",
                "facility_name": "Facility 1",
            }
        }
    )
