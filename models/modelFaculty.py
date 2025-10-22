from pydantic import BaseModel, Field
from typing import List
from utils.util_response import ResponseModel

class FacultyBase (BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="Nama Fakultas"
    )
    status: bool = Field(
        ...,
        title="Status",
        description="Status Fakultas"
    )

class FacultyEx (FacultyBase):
    email: str | None = Field (
        None,
        title="Email",
        description="Email Fakultas"
    )
class FacultyProdiId (BaseModel):
    prodiId: List[str] | None = Field(
        default=None,
        title="Prodi",
        description="Prodi Fakultas"
    )
    
class FacultyRequestUpdate (BaseModel):
    name: str | None = Field(
        None,
        title="Name",
        description="Nama Fakultas"
    )
    status: bool | None = Field(
        None,
        title="Status",
        description="Status Fakultas"
    )
    email: str | None = Field (
        None,
        title="Email",
        description="Email Fakultas"
    )
    
class FacultyRequestCreate (FacultyEx):
    pass

class FacultyCreate (FacultyRequestCreate):
    isDeleted: bool = Field(
        False
    )

class FacultyId (BaseModel):
    id: str = Field(
        ...,
        alias="_id"
    )
        
class FacultyView (FacultyEx, FacultyId):
    pass

class ResponseFacultyView (ResponseModel):
    data: FacultyView

class FacultyViewAll (BaseModel):
    page: int
    size: int
    total_items: int
    total_pages: int
    items: list[FacultyView]
    