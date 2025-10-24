
from fastapi import FastAPI
from routers.routeProdi import ApiRouter_Prodi
from routers.routerFaculty import ApiRouter_Faculty
from routers.routerMahasiswa import ApiRouter_Mahasiswa
from routers.routerMatkul import ApiRouter_Matkul

app = FastAPI(
    title="Belajar FastAPI",
    description="Belajar FastAPI",
    docs_url="/swgr"
)
    
app.include_router(ApiRouter_Faculty)
app.include_router(ApiRouter_Prodi)
app.include_router(ApiRouter_Matkul)
app.include_router(ApiRouter_Mahasiswa)