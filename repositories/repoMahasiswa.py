from typing import Any

from bson import ObjectId
from controllers.controllerFaculty import FacultyController
from controllers.controllerProdi import ProdiController
from models.modelMahasiswa import MahasiswaRequestCreate, MahasiswaView
from mongodb.mongoCollection import TbMahasiswa


class MahasiswaRepository:
    @staticmethod
    async def GetById(
        mahasiswaId: str
    ) -> MahasiswaView | None:
        query: dict["str", Any] = {
            "isDeleted": False,
            "_id": ObjectId(mahasiswaId)
        }
        data = TbMahasiswa.find_one(query)
        
        if not data:
            return None
    
        fetchProdi = await ProdiController.GetById(str(data["prodiId"]))
        fetchFaculty = await FacultyController.GetById(str(data["facultyId"]))
        
        data["prodiName"] = fetchProdi.name
        data["facultyName"] = fetchFaculty.name
        data["_id"] = str(data["_id"])
        data["prodiId"] = str(data["prodiId"])
        data["facultyId"] = str(data["facultyId"])
        return MahasiswaView (**data)
    
    @staticmethod
    async def Create(
        param: MahasiswaRequestCreate
    ) -> str | None :
        convertedParam = param.model_dump()
        convertedParam["prodiId"] = ObjectId(param.prodiId)
        convertedParam["facultyId"] = ObjectId(param.facultyId)
        
        data = TbMahasiswa.insert_one(convertedParam)
        
        if not data:
            return None
        
        return str(data.inserted_id)