import re
from typing import Any
from fastapi import HTTPException
from models.modelFaculty import FacultyCreate, FacultyRequestCreate, FacultyRequestUpdate, FacultyView
from mongodb.mongoCollection import TbFaculty
from repositories.repoFaculty import FacultyRepository

class FacultyController:
    @staticmethod
    def Find(
        name: str | None,
        size: int,
        page: int
    ) -> dict[str, Any]:
        query: dict[str, Any] = {
            "isDeleted": False
        }
        if name:
            query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}

        total_items = TbFaculty.count_documents(query)
        total_pages = (total_items + size - 1) // size if total_items > 0 else 0

        start = (page - 1) * size
        if start >= total_items and total_items > 0:
            raise HTTPException(
                status_code=404,
                detail=f"Halaman {page} tidak ditemukan (total halaman {total_pages})"
            )

        faculties = list(
            TbFaculty.find(query)
            .skip(start)
            .limit(size)
        )
        
        for f in faculties:
            f["_id"] = str(f["_id"])

        return {
            "data": {
                "page": page,
                "size": size,
                "total_items": total_items,
                "total_pages": total_pages,
                "items": faculties
            }
        }
    
    @staticmethod
    async def GetById(
        facultyId: str
    ) -> FacultyView:
        data = await FacultyRepository.GetById(
            facultyId
        )
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Faculty not found"
            )
        
        return data
    
    @staticmethod
    async def Create(
        param: FacultyRequestCreate
    ):
        newDataId = await FacultyRepository.Create(
            FacultyCreate(
                name=param.name,
                status=param.status,
                email=param.email,
                isDeleted=False
            )
        )
        
        if not newDataId:
            raise HTTPException(
                status_code=500,
                detail="Failed to Create Faculty"
            )
        
        return newDataId
    
    @staticmethod
    async def Update(
        facultyId: str,
        param: FacultyRequestUpdate
    ):
        currentData: FacultyView = await FacultyController.GetById(
            facultyId
        )
        
        extracted: dict[str, Any] = param.model_dump() # this will comeout as {"name": "string", "status": bool, "email": "string"}
        for e in param.model_dump():
            if extracted[e] is None:
                extracted.pop(e)
        
        print(extracted)
        
        if not await FacultyRepository.Update(
            currentData.id,
            extracted
        ):
            raise HTTPException(
                status_code=500,
                detail="Failed to Update Faculty"
            )
        return currentData.id
    
    @staticmethod
    async def Delete(
        facultyId: str,
    ):
        currentData = await FacultyController.GetById(
            facultyId
        )
        
        if not await FacultyRepository.Update(
            currentData.id,
            param={
                "isDeleted": True
            }
        ):
            raise HTTPException(
                status_code=500,
                detail="Failed to Delete Product"
            )
        
        return currentData.id
        
        