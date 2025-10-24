from fastapi import APIRouter, HTTPException, Query

from controllers.controllerMahasiswa import MahasiswaController
from models.modelMahasiswa import MahasiswaRequestCreate, RespondMahasiswaView


ApiRouter_Mahasiswa = APIRouter(
    prefix="/mahasiswa",
    tags=["Mahasiswa"]
)

@ApiRouter_Mahasiswa.get(
    "/find",
    summary="Get All Mahasiswa",
)
async def ApiRouter_Mahasiswa_Find(
    name: str = Query(default=None, description="Nama Mahasiswa"),
    prodiId: str = Query(default=None, description="ID Prodi"),
    facultyId: str = Query(default=None, description="ID Fakultas"),
    size: int = Query(default=10, ge=1, le=100, description="Jumlah data per halaman"),
    page: int = Query(default=1, ge=1, description="Nomor halaman")
):
    data = await MahasiswaController.Find(
        name=name,
        prodiId=prodiId,
        facultyId=facultyId,
        size=size,
        page=page
    )
    return {
        "data": data
    }
    
@ApiRouter_Mahasiswa.get(
    "/{mahasiswaId}",
    summary="Get Mahasiswa by Id",
    response_model=RespondMahasiswaView
)
async def ApiRoute_Get_Mahasiswa_Id(
    mahasiswaId: str
):
    data = await MahasiswaController.GetById(mahasiswaId)
    return RespondMahasiswaView(
        status_code=200,
        message="Success Get Data",
        data=data
    )
    
@ApiRouter_Mahasiswa.post(
    "/create", 
    summary="Create Mahasiswa",
    response_model=RespondMahasiswaView
)
async def ApiRoute_Create_Mahasiswa(
    req: MahasiswaRequestCreate
):
    newMahasiswaId = await MahasiswaController.Create(
        param=req
    )
    
    if not newMahasiswaId:
        raise HTTPException(
            status_code=500,
            detail="Gagal membuat Mata Kuliah"
        )
    
    data = await MahasiswaController.GetById(
        newMahasiswaId
    )
    
    return RespondMahasiswaView(
        status_code=200,
        message="Success Create Mahasiswa",
        data=data
    )