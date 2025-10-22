from pydantic import BaseModel, Field
# from relationships.relationshipProdi import ProdiFaculty
from utils.util_response import ResponseModel

class ProdiId (BaseModel):
    id: str = Field(
        ...,
        alias="_id"
    )

class ProdiBase (BaseModel):
    name: str = Field(
        ...,
        title="Nama Prodi",
        description="Nama Prodi"
    )
    lecturer: str = Field(
        ...,
        title="Lecturer",
        description="Nama Dosen"
    )
    
class ProdiEx(ProdiBase):
    facultyId: str = Field(
        ...,
        title="Faculty ID",
        description="Faculty ID"
    )

class ProdiRequestCreate (ProdiEx):
    pass

class ProdiCreate (ProdiRequestCreate):
    isDeleted: bool = Field(
        False
    )
    
class ProdiFacultyResponse (BaseModel):
    facultyName: str = Field(
        default=...,
    )
    
class ProdiView (ProdiFacultyResponse, ProdiEx, ProdiId):
    pass

class ResponseProdiView(ResponseModel):
    data: ProdiView
    
class ProdiViewAll (BaseModel):
    page: int
    size: int
    total_items: int
    total_pages: int
    items: list[ProdiView]