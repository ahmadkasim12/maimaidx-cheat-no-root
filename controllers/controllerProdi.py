import re
from typing import Any
from bson import ObjectId
from fastapi import HTTPException

from controllers.controllerFaculty import FacultyController
from models.modelProdi import ProdiCreate, ProdiRequestCreate, ProdiView, ProdiViewAll
from mongodb.mongoCollection import TbProdi
from repositories.repoProdi import ProdiRepository


class ProdiController:
    @staticmethod
    def Find(
        name: str | None,
        facultyId : str | None,
        size: int,
        page: int
    ) -> ProdiViewAll:
        query: dict[str, Any] = {
            "isDeleted": False
        }
        if name:
            query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
        
        if facultyId:
            query["facultyId"] = ObjectId(facultyId)

        total_items = TbProdi.count_documents(query)
        total_pages = (total_items + size - 1) // size if total_items > 0 else 0

        start = (page - 1) * size
        if start >= total_items and total_items > 0:
            raise HTTPException(
                status_code=404,
                detail=f"Halaman {page} tidak ditemukan (total halaman {total_pages})"
            )

        prodi = list(
            TbProdi.find(query)
            .skip(start)
            .limit(size)
        )
        
        for p in prodi:
            p["_id"] = str(p["_id"])
            if p["facultyId"] is not None:
                newFacultyId = str(p["facultyId"])
                data = FacultyController.GetById(newFacultyId)
                p["facultyName"] = data.name
                p["facultyId"] = newFacultyId
                
        return ProdiViewAll(
            page=page,
            size=size,
            total_items=total_items,
            total_pages=total_pages,
            items=prodi
        )
    
    @staticmethod
    def GetById(
        prodiId: str
    ) -> ProdiView:
        data = ProdiRepository.GetById(prodiId)
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Prodi not found"
            )
            
        # newFacultyId = FacultyController.GetById(str(data.facultyId))
        return data
    
    @staticmethod
    def Create(
        param: ProdiRequestCreate
    ) -> str:
        newProdiId = ProdiRepository.Create(
            ProdiCreate(
                name=param.name,
                lecturer=param.lecturer,
                facultyId=param.facultyId,
                isDeleted=False
            )
        )
        
        if not newProdiId:
            raise HTTPException(
                status_code=500,
                detail="Failed to create Prodi"
            )
        
        facultyIdFetch = FacultyController.GetById(param.facultyId)
        
        if not facultyIdFetch:
             raise HTTPException(
                status_code=500,
                detail="Faculty does not exist"
            )
             
        return newProdiId
        