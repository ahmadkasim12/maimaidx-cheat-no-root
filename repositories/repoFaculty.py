from typing import Any
from bson import ObjectId
from models.modelFaculty import FacultyRequestCreate, FacultyView
from mongodb.mongoCollection import TbFaculty

class FacultyRepository:
    @staticmethod
    async def GetById(
        facultyId: str
    ) -> FacultyView | None:
        query: dict[str, Any] = {
            "isDeleted": False,
            "_id": ObjectId(facultyId)
        }
        product = TbFaculty.find_one(query)
        if not product:
            return None
        else:
            product["_id"] = str(product["_id"])
            return FacultyView (**product)
    
    @staticmethod
    async def Create(
        param: FacultyRequestCreate
    ):
        result = TbFaculty.insert_one(param.model_dump())
        return str(result.inserted_id)
    
    @staticmethod
    async def Update(
        facultyId: str,
        param: dict[str, Any]
    ):
        print(param)
        result = TbFaculty.update_one(
            {"_id": ObjectId(facultyId)},
            {"$set": param}
        )

        return (result.matched_count == 1)