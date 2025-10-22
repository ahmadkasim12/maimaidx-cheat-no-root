
from fastapi import FastAPI
from routers.routeProdi import ApiRouter_Prodi
from routers.routerFaculty import ApiRouter_Faculty

app = FastAPI(
    title="Belajar FastAPI",
    description="Belajar FastAPI",
    docs_url="/swgr"
)
    
app.include_router(ApiRouter_Faculty)
app.include_router(ApiRouter_Prodi)