from datetime import datetime

from src.apps.authentication.schema import User
from src.db.crud.mongo_crud import MongoBaseCrud
from src.db.mongo_init import MongoDBClient
from src.db.mongo_collection_config import CollectionNameRegistry


async def fetch_user_details_dao(query: dict, projection: dict = {}):
    """
    Fetch user details from mongodb
    :param query: dict
    :param projection: dict
    """
    query.update({"is_active": True})
    return await MongoBaseCrud.fetch(
        key=query,
        find_one=True,
        projection=projection,
        collection_name=CollectionNameRegistry.USER,
    )


async def create_user_dao(q_request: dict):
    """
    Create user in mongodb
    :param q_request: dict
    """
    q_request = User(**q_request)
    return await MongoBaseCrud.create(
        item=q_request.model_dump(), collection_name=CollectionNameRegistry.USER
    )


async def update_user_dao(find_query: dict, update_query: dict):
    find_query.update({"is_active": True})
    update_query.update({"is_new_user": False, "modified_at": datetime.utcnow()})
    return await MongoBaseCrud.update(
        key=find_query,
        item=update_query,
        collection_name=CollectionNameRegistry.USER,
    )


