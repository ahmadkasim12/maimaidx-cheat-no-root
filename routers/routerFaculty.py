from fastapi import APIRouter, Body, Path, Query

from controllers.controllerFaculty import FacultyController
from models.modelFaculty import FacultyRequestCreate, FacultyRequestUpdate, ResponseFacultyView
from utils.util_response import ResponseModelObjectId


ApiRouter_Faculty = APIRouter(
    prefix="/faculty",
    tags=["Faculty"]
)

@ApiRouter_Faculty.get(
    "/find",
    summary="Get All Faculties",
)
async def ApiRouter_Faculty_Find(
    name: str = Query(default=None, description="Nama Fakultas"),
    size: int = Query(default=10, ge=1, le=100, description="Jumlah data per halaman"),
    page: int = Query(default=1, ge=1, description="Nomor halaman")
):
    data = FacultyController.Find(
        name=name,
        size=size,
        page=page
    )
    return data

@ApiRouter_Faculty.get(
    "/get/{facultyId}",
    response_model=ResponseFacultyView,
    summary="Get Faculty by Id"
)
async def ApiRouter_Faculty_GetById(
    facultyId: str
):
    data = FacultyController.GetById(
        facultyId
    )
    
    return ResponseFacultyView(
        status_code=200,
        message="Success Get Data",
        data=data
)

@ApiRouter_Faculty.post(
    "/create",
    response_model=ResponseFacultyView,
    summary="Create Faculty"
)
async def ApiRouter_Faculty_Create(
     req: FacultyRequestCreate = Body(
        default=...,
    )
):
    newFacultyId = FacultyController.Create(
        param=req
    )
    
    data = FacultyController.GetById(
        newFacultyId
    )
    
    return ResponseFacultyView(
        status_code=200,
        message="Success Create Data",
        data=data
    )
    
@ApiRouter_Faculty.put(
    "/update/{facultyId}",
    response_model=ResponseFacultyView,
    summary="Update Faculty by Id"
)
async def ApiRouter_Faculty_Update(
    facultyId: str,
    req: FacultyRequestUpdate = Body(
        default=...,
    )
):
    updatedProductId = FacultyController.Update(
        facultyId,
        req
    )
    
    data = FacultyController.GetById(
        updatedProductId
    )
    
    return ResponseFacultyView(
        status_code=200,
        message="Success Update Data",
        data=data
    )
    
@ApiRouter_Faculty.delete(
    "/delete/{facultyId}",
    response_model=ResponseModelObjectId,
    summary="Delete Faculty by Id"
)
async def ApiRouter_Faculty_Delete(
    facultyId: str = Path(
        default=...,
    ),
):
    deletedProductId = FacultyController.Delete(
        facultyId
    )
    
    return ResponseModelObjectId(
        status_code=200,
        message="Success Update Data",
        data=deletedProductId
    )