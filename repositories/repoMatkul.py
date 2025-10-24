from typing import Any
from bson import ObjectId
from controllers.controllerProdi import ProdiController
from models.modelMatkul import MatkulRequestCreate, MatkulView
from mongodb.mongoCollection import TbMatkul


class MatkulRepository:
    @staticmethod
    async def GetById(
        matkulId: str
    ) -> MatkulView | None:
        query: dict["str", Any] = {
            "isDeleted": False,
            "_id": ObjectId(matkulId)
        }
        data = TbMatkul.find_one(query)
        
        if not data:
            return None
        
        if data["prodiId"]:
            prodi = await ProdiController.GetById(str(data["prodiId"]))
            data["prodiId"] = str(data["prodiId"])
            data["prodiName"] = prodi.name
        
        data["_id"] = str(data["_id"])
        return MatkulView (**data)
    
    @staticmethod
    def Create(
        param: MatkulRequestCreate
    ) -> str | None:
        newParam = param.model_dump()
        newParam["prodiId"] = ObjectId(param.prodiId)
        newProdiId = TbMatkul.insert_one(newParam)
        return str(newProdiId.inserted_id)