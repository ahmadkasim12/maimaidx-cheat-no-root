from fastapi import APIRouter, HTTPException, Query
from controllers.controllerMatkul import MatkulController
from models.modelMatkul import MatkulRequestCreate, ResponseMatkulView


ApiRouter_Matkul = APIRouter(
    prefix="/matkul",
    tags=["Matkul"]
)

@ApiRouter_Matkul.get(
    "/find",
    summary="Get All Matkul",
)
async def ApiRouter_Matkul_Find(
    name: str = Query(default=None, description="Nama Fakultas"),
    prodiId: str = Query(default=None, description="ID Prodi"),
    size: int = Query(default=10, ge=1, le=100, description="Jumlah data per halaman"),
    page: int = Query(default=1, ge=1, description="Nomor halaman")
):
    data = await MatkulController.Find(
        name=name,
        prodiId=prodiId,
        size=size,
        page=page
    )
    return {
        "data": data
    }
    
@ApiRouter_Matkul.get(
    "/{matkulId}",
    summary="Get Matkul by Id",
    response_model=ResponseMatkulView
)
async def ApiRoute_Get_Matkul_Id(
    matkulId: str
):
    data = await MatkulController.GetById(matkulId)
    
    return ResponseMatkulView(
        status_code=200,
        message="Success Get Data",
        data=data
    )
    
@ApiRouter_Matkul.post(
    "/create",
    response_model=ResponseMatkulView,
    summary="Create Matkul",
)
async def ApiRoute_Create_Matkul(
    req: MatkulRequestCreate
):
    newMatkulId = MatkulController.Create(req)
    
    if not newMatkulId:
        raise HTTPException(
            status_code=500,
            detail="Gagal membuat Mata Kuliah"
        )
    data = await MatkulController.GetById(newMatkulId)
    
    return ResponseMatkulView(
        status_code=200,
        message="Success Create Data",
        data=data
    )