from pydantic import BaseModel, Field


class MatkulProdiId (BaseModel):
    prodiId: str = Field(
        ...,
        title="ID Prodi",
        description="ID Prodi"
    )
    
class MatkulProdiName (BaseModel):
    prodiName: str | None = Field(
        None,
        title="Nama Prodi",
        description="Nama Prodi"
    )