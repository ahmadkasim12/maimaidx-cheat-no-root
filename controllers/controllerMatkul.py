import re
from typing import Any

from bson import ObjectId
from fastapi import HTTPException
from models.modelMatkul import MatkulCreate, MatkulRequestCreate, MatkulView, MatkulViewAll
from mongodb.mongoCollection import TbMatkul
from repositories.repoMatkul import MatkulRepository
from repositories.repoProdi import ProdiRepository


class MatkulController:
    @staticmethod
    async def Find(
        name: str | None,
        prodiId: str | None,
        size: int,
        page: int
    ) -> MatkulViewAll :
        query: dict[str, Any] = {
            "isDeleted": False
        }
        if name:
            query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
            
        if prodiId:
            query["prodiId"] = ObjectId(prodiId)
            
        total_items = TbMatkul.count_documents(query)
        total_pages = (total_items + size - 1) // size if total_items > 0 else 0

        start = (page - 1) * size
        if start >= total_items and total_items > 0:
            raise HTTPException(
                status_code=404,
                detail=f"Halaman {page} tidak ditemukan (total halaman {total_pages})"
            )

        matkul = list(
            TbMatkul.find(query)
            .skip(start)
            .limit(size)
        )
        
        for m in matkul:
            m["_id"] = str(m["_id"])
            data = await ProdiRepository.GetById(m["prodiId"])
            
            if not data:
                raise HTTPException(
                    status_code=500,
                    detail="Data Prodi terkait tidak ditemukan"
                )
            
            m["prodiId"] = str(m["prodiId"])
            m["prodiName"] = data.name
            
        return MatkulViewAll(
            page=page,
            size=size,
            total_items=total_items,
            total_pages=total_pages,
            items=matkul
        )
    
    @staticmethod
    async def GetById(
        matkulId: str
    ) -> MatkulView:
        
        data = await MatkulRepository.GetById(matkulId)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail="Mata Kuliah tidak ditemukan"
            )
        
        return data
    
    @staticmethod
    def Create(
        param: MatkulRequestCreate
    ) -> str | None:
        
        newId = MatkulRepository.Create(MatkulCreate(
            name=param.name,
            sks=param.sks,
            prodiId=param.prodiId,
            isDeleted=False
        ))
        
        if not newId:
            raise HTTPException(
                status_code=500,
                detail="Gagal membuat Mata Kuliah"
            )
        
        return newId
        