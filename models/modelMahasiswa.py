from pydantic import BaseModel, Field

from relationships.relationshipMahasiswa import MahasiswaRelationship
from utils.util_response import ResponseModel

class MahasiswaId (BaseModel):
    id: str = Field(
        ...,
        alias="_id"
    )

class MahasiswaBase (BaseModel):
    name: str = Field(
        ...,
        title="Nama Mahasiswa",
        description="Nama lengkap mahasiswa")
    facultyId: str = Field(
        ...,
        title="ID Fakultas",
        description="ID Fakultas tempat mahasiswa terdaftar")
    prodiId: str = Field(
        ...,
        title="ID Prodi",
        description="ID Prodi tempat mahasiswa terdaftar")
    
class MahasiswaRequestCreate (MahasiswaBase):
    pass

class MahasiswaCreate (MahasiswaRequestCreate):
    isDeleted: bool = Field(
        False
    )
    
class MahasiswaView (MahasiswaRelationship, MahasiswaBase, MahasiswaId):
    pass

class RespondMahasiswaView (ResponseModel):
    data: MahasiswaView
    
class MahasiswaViewAll (BaseModel):
    page: int
    size: int
    total_items: int
    total_pages: int
    items: list[MahasiswaView]
