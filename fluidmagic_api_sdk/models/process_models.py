"""Collection of entities used in the api."""

from pydantic import BaseModel, ConfigDict, Field

from .data_models.process_data import ProcessData
from .enums import TankType


class TankModelShort(BaseModel, extra="ignore"):
    name: str = Field(..., description="Tank name.")
    tank_type: TankType = Field(..., description="Tank type.")


class ProcessModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_id: str = Field(..., description="Facility identifier.")
    name: str = Field(..., description="Name of process model.")
    description: str = Field(..., description="Description of process model.")
    process_data: ProcessData = Field(..., description="Data that defines the process model.")
    created_by: str = Field(..., description="User or application that created process model.")
    created_date: str = Field(..., description="Date model was created.")

    def get_implicit_component_count(self) -> int:
        """Get the number of implicit components in the process model."""
        return self.process_data.get_implicit_component_count()


class ProcessReturnModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    facility_id: str = Field(..., description="Facility identifier.")
    name: str = Field(..., description="Name of process model.")
    description: str = Field(..., description="Description of process model.")
    tanks: list[TankModelShort] = Field(..., description="List of tanks in the process model.")
    implicit_component_count: int | None = Field(None, description="Number of components if valid. -1 if not valid.")
    process_data: ProcessData = Field(..., description="Data that defines the process model.")
    created_by: str = Field(..., description="User or application that created model.")
    created_date: str = Field(..., description="Date model was created.")

    @staticmethod
    def create_from_process_model(process_model: "ProcessModel") -> "ProcessReturnModel":
        item = process_model.model_dump()

        tanks = process_model.process_data.tanks

        item["tanks"] = [{"name": tank.name, "tank_type": tank.tank_type} for tank in tanks]
        item["implicit_component_count"] = process_model.process_data.get_implicit_component_count()

        return ProcessReturnModel(**item)


class ProcessOverviewModel(BaseModel, extra="ignore"):
    id: str = Field(..., description="Unique identifier.")
    name: str = Field(..., description="Name of process model.")
    description: str = Field(..., description="Description of process model.")
    tanks: list[TankModelShort] = Field(..., description="List of tanks in the process model.")
    implicit_component_count: int | None = Field(None, description="Number of components if valid. -1 if not valid.")

    @staticmethod
    def create_from_process_model(process_model: "ProcessModel") -> "ProcessOverviewModel":
        item = process_model.model_dump()

        tanks = process_model.process_data.tanks
        item["tanks"] = [{"name": tank.name, "tank_type": tank.tank_type} for tank in tanks]
        item["implicit_component_count"] = process_model.process_data.get_implicit_component_count()

        return ProcessOverviewModel(**item)


class ProcessCreateModel(BaseModel, extra="ignore"):
    name: str = Field(..., description="Name of model.")
    description: str = Field(..., description="Description of model.")
    process_data: ProcessData = Field(..., description="Data that defines the process model.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "process_model_1",
                "description": "Example process model.",
                "process_data": {
                    "name": "process_1",
                    "tanks": [
                        {
                            "name": "sep_1",
                            "tank_type": "kval",
                            "pressure": 100.0,
                            "temperature": 50.0,
                            "oil_destination": "oil_1",
                            "gas_destination": "gas_1",
                            "process_factor": {
                                "name": "process_factor_1",
                                "table_type": "kvaltable",
                                "table": [[1.0, 2.0, 3.0, 4.0], [3.0, 4.0, 5.0, 6.0]],
                                "plus_index": 2,
                            },
                        },
                        {
                            "name": "oil_1",
                            "tank_type": "oiltank",
                            "pressure": 100.0,
                            "temperature": 50.0,
                        },
                        {
                            "name": "gas_1",
                            "tank_type": "gastank",
                            "pressure": 100.0,
                            "temperature": 50.0,
                        },
                    ],
                },
            }
        }
    )
