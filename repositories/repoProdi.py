from typing import Any

from bson import ObjectId
from controllers.controllerFaculty import FacultyController
from models.modelProdi import ProdiRequestCreate, ProdiView
from mongodb.mongoCollection import TbProdi


class ProdiRepository:
    @staticmethod
    async def GetById(
        prodiId: str
    ) -> ProdiView | None:
        query: dict[str, Any] = {
            "isDeleted": False,
            "_id": ObjectId(prodiId)
        }
        prodi = TbProdi.find_one(query)
        if not prodi:
            return None
        
        if prodi["facultyId"]:
            data = await FacultyController.GetById(str(prodi["facultyId"]))
            prodi["facultyId"] = str(prodi["facultyId"])
            prodi["facultyName"] = data.name
        
        prodi["_id"] = str(prodi["_id"])
        return ProdiView (**prodi)
        
    @staticmethod
    async def Create(
        param: ProdiRequestCreate
    ) -> str | None:
        newParam = param.model_dump()
        newParam["facultyId"] = ObjectId(newParam["facultyId"])
        
        
        result = TbProdi.insert_one(newParam)
        return str(result.inserted_id)