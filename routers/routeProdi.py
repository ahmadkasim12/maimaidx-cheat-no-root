from fastapi import APIRouter, Body, Query

from controllers.controllerProdi import ProdiController
from models.modelProdi import ProdiRequestCreate, ResponseProdiView


ApiRouter_Prodi = APIRouter(
    prefix="/prodi",
    tags=["Prodi"]
)

@ApiRouter_Prodi.get(
    "/find",
    summary="Get All Prodi"
)
def ApiRouter_Prodi_Find(
    name: str = Query(default=None, description="Nama Prodi"),
    facultyId: str = Query(default=None, description="Fakultas ID"),
    size: int = Query(default=10, ge=1, le=100, description="Jumlah data per halaman"),
    page: int = Query(default=1, ge=1, description="Nomor halaman")
):
    data = ProdiController.Find(
        name=name,
        facultyId=facultyId,
        size=size,
        page=page
    )
    return {
        "data": data
    }
    
@ApiRouter_Prodi.get(
    "/{prodiId}",
    summary="Get Prodi by Id",
    response_model=ResponseProdiView
)
def ApiRoute_Get_Prodi_Id(
    prodiId: str
):
    data = ProdiController.GetById(prodiId)
    
    return ResponseProdiView(
        status_code=200,
        message="Success Get Data",
        data=data
    )
    
@ApiRouter_Prodi.post(
    "/create",
    response_model=ResponseProdiView,
    summary="Create Prodi",
)
def ApiRoute_Create_Prodi(
    req: ProdiRequestCreate = Body(
        ...
    )
):
    newProdiId = ProdiController.Create(req)
    
    data = ProdiController.GetById(newProdiId)
    
    return ResponseProdiView(
        status_code=200,
        message="Success Get Data",
        data=data
    )
    