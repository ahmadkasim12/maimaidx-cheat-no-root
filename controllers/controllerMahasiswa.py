from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from controllers.controllerFaculty import FacultyController
from controllers.controllerProdi import ProdiController
from models.modelMahasiswa import MahasiswaCreate, MahasiswaRequestCreate, MahasiswaView, MahasiswaViewAll
from mongodb.mongoCollection import TbMahasiswa
from repositories.repoMahasiswa import MahasiswaRepository


class MahasiswaController:
    @staticmethod
    async def Find(
        name: str | None,
        prodiId: str | None,
        facultyId: str | None,
        size: int,
        page: int
    ) -> MahasiswaViewAll :
        query: dict[str, Any] = {
            "isDeleted": False
        }
        if name:
            query["name"] = {"$regex": re.compile(name, re.IGNORECASE)} # type: ignore
            
        if prodiId:
            query["prodiId"] = ObjectId(prodiId)
            
        if facultyId:
            query["facultyId"] = ObjectId(facultyId)
            
        total_items = TbMahasiswa.count_documents(query)
        total_pages = (total_items + size - 1) // size if total_items > 0 else 0

        start = (page - 1) * size
        if start >= total_items and total_items > 0:
            raise HTTPException(
                status_code=404,
                detail=f"Halaman {page} tidak ditemukan (total halaman {total_pages})"
            )

        mahasiswa = list(
            TbMahasiswa.find(query)
            .skip(start)
            .limit(size)
        )
        
        for m in mahasiswa:
            m["_id"] = str(m["_id"])
            fetchProdi = await ProdiController.GetById(str(m["prodiId"]))
            fetchFaculty = await FacultyController.GetById(str(m["facultyId"]))
            
            if not fetchProdi:
                raise HTTPException(
                    status_code=500,
                    detail="Data Prodi terkait tidak ditemukan"
                )
                
            if not fetchFaculty:
                raise HTTPException(
                    status_code=500,
                    detail="Data Fakultas terkait tidak ditemukan"
                )
            
            m["prodiId"] = str(m["prodiId"])
            m["prodiName"] = fetchProdi.name
            m["facultyId"] = str(m["facultyId"])
            m["facultyName"] = fetchFaculty.name
            
        return MahasiswaViewAll(
            page=page,
            size=size,
            total_items=total_items,
            total_pages=total_pages,
            items=mahasiswa
        )
        
    @staticmethod
    async def GetById(
        mahasiswaId: str
    ) -> MahasiswaView :
        data = await MahasiswaRepository.GetById(mahasiswaId)
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Mahasiswa tidak ditemukan"
            )
        return data
    
    @staticmethod
    async def Create(
        param: MahasiswaRequestCreate
    ) -> str | None:
        
        fetchProdi = await ProdiController.GetById(param.prodiId)
        if not fetchProdi:
            raise HTTPException(
                status_code=404,
                detail="Prodi tidak ditemukan"
            )
        fetchFaculty = await FacultyController.GetById(param.facultyId)
        if not fetchFaculty:
            raise HTTPException(
                status_code=404,
                detail="Fakultas tidak ditemukan"
            )
        
        newId = await MahasiswaRepository.Create(MahasiswaCreate(
            name=param.name,
            prodiId=param.prodiId,
            facultyId=param.facultyId,
            isDeleted=False
        ))
        
        if not newId:
            raise HTTPException(
                status_code=500,
                detail="Gagal membuat Mahasiswa"
            )
            
        return newId