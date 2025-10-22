from pydantic import BaseModel, Field

from models.modelFaculty import FacultyView


class ProdiFaculty (BaseModel):
    faculty: FacultyView | None = Field(
        None,
    )