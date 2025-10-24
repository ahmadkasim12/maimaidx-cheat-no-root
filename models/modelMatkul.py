from pydantic import BaseModel, Field
from relationships.relationshipMatkul import MatkulProdiId, MatkulProdiName
from utils.util_response import ResponseModel


class MatkulBase (BaseModel):
    name: str = Field(
        ...,
        title="Mata Kuliah",
        description="Mata Kuliah"
    )
    sks: int = Field(
        ...,
        title="Satuan Kredit Semester",
        description="Satuan Kredit Semester"
    )
    
class MatkulEx (MatkulProdiId, MatkulBase):
    pass

class MatkulId (BaseModel):
    id: str = Field(
        ...,
        alias="_id"
    )

class MatkulRequestCreate(MatkulEx):
    pass

class MatkulCreate(MatkulRequestCreate):
    isDeleted: bool = Field(
        False,
    )

class MatkulView (MatkulProdiName, MatkulEx, MatkulId):
    pass

class ResponseMatkulView (ResponseModel):
    data: MatkulView
    
class MatkulViewAll (BaseModel):
    page: int
    size: int
    total_items: int
    total_pages: int
    items: list[MatkulView]