from pydantic import BaseModel, Field


class MahasiswaRelationship (BaseModel):
    prodiName: str = Field(
        ...,
    )
    facultyName: str = Field(
        ...,
    )