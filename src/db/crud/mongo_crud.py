from dateutil.tz import gettz
from pymongo import DESCENDING
from src.core.logger_config import dblogger as logger
from src.db.db_exceptions import (
    CreateException,
    CollectionNotProvidedException,
    DeleteException,
    MongoDatabaseException,
)
from src.db.mongo_init import MongoDBClient

timezone = gettz("Asia/Kolkata")
FIND_MAX_ITEM = 250

required_fields = "Required fields to preform action are collection_name: str"


class MongoBaseCrud:

    @classmethod
    async def create(cls, **kwargs):
        """
        The create function creates a new record in the database.
            Args:
                collection_name (str): The name of the collection to create a record in.
                item (dict): A dictionary containing all the fields and values for this new record.

        :param cls: Pass the class name of the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A pymongo
        """
        collection_name = kwargs.get("collection_name")
        if not collection_name:
            raise CollectionNotProvidedException(
                message=f"Please provide collection name. {required_fields}, item: dict."
            )
        item = kwargs.get("item")
        if not item:
            raise CreateException(
                message=f"Please provide data to create record. {required_fields}, item: dict."
            )
        try:
            result = await MongoDBClient().db[collection_name].insert_one(item)
        except Exception as e:
            logger.exception(e)
            raise MongoDatabaseException(message="Unable to insert record.")
        return result

    @classmethod
    async def update(
        cls,
        key,
        upsert: bool = False,
        update_many: bool = False,
        sort_by_latest: bool = False,
        **kwargs,
    ):
        """
        The update function updates a record in the database.
            Args:
                key (dict): The key to search for in the collection.
                upsert (bool, optional): If True, creates a new document when no document matches the query criteria.
                Defaults to False.

        :param cls: Make the function a class method
        :param key: Find the document to update
        :param upsert: bool: Insert the data if it is not present in the collection
        :param **kwargs: Pass a keyworded, variable-length argument list
        :return: A pymongo
        """
        collection_name = kwargs.get("collection_name")
        if not collection_name:
            raise CollectionNotProvidedException(
                message=f"Please provide collection name. {required_fields}, key: dict, item: dict."
            )
        item = kwargs.get("item")
        if not item:
            raise CreateException(
                message=f"Please provide data to update record. {required_fields}, key: dict, item: dict."
            )
        try:
            if update_many:
                await MongoDBClient().db[collection_name].update_many(
                    key, {"$set": item}, upsert
                )
            elif sort_by_latest:
                latest_obj = (
                    await MongoDBClient()
                    .db[collection_name]
                    .find_one(key, sort=[("_id", -1)])
                )
                if latest_obj:
                    logger.info("Updating latest object in collection.")
                    key = {"_id": latest_obj["_id"]}
                await MongoDBClient().db[collection_name].update_one(
                    key, {"$set": item}, upsert
                )
            else:
                await MongoDBClient().db[collection_name].update_one(
                    key, {"$set": item}, upsert
                )
        except Exception as e:
            logger.exception(e)
            raise MongoDatabaseException(
                message=f"Error occurred while searching data for key {key}"
            )

        logger.info(
            f"data {item} with key: {key}, collection: {collection_name} is successfully updated"
        )

    @classmethod
    async def fetch(cls, key, find_one: bool = False, **kwargs) -> list:
        """
        The fetch function is used to fetch data from the database.
            Args:
                key (dict): The key for which we want to fetch data.
                find_one (bool, optional): If True, it will return only one record. Defaults to False.

        :param cls: Pass the class object to the function
        :param key: Specify the condition for which we want to fetch data from the database
        :param find_one: bool: Find one record or all records
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: The data in the form of list
        """
        collection_name = kwargs.get("collection_name")
        projection = kwargs.get("projection", {})

        if not collection_name:
            raise CollectionNotProvidedException(
                message=f"Please provide collection name. {required_fields}, key: dict."
            )
        responses = []
        try:
            if find_one:
                result = (
                    await MongoDBClient()
                    .db[collection_name]
                    .find_one(
                        key,
                        sort=[("_id", DESCENDING)],
                        projection=projection,
                    )
                )
                responses.append(result) if result else []
            else:
                responses = (
                    MongoDBClient().db[collection_name].find(key, projection=projection)
                )
                responses = await responses.to_list(length=FIND_MAX_ITEM)
        except Exception as e:
            logger.exception(e)
            raise MongoDatabaseException(
                message=f"Unable to fetch record for {key} in {collection_name} collection"
            )

        logger.info(f"{len(responses)} data found for query: {key}")
        return responses

    @classmethod
    async def bulk_create(cls, **kwargs):
        """
        The create function creates a new record in the database.
            Args:
                collection_name (str): The name of the collection to create a record in.
                item (dict): A dictionary containing all the fields and values for this new record.

        :param cls: Pass the class name of the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A pymongo
        """
        collection_name = kwargs.get("collection_name")
        if not collection_name:
            raise CollectionNotProvidedException(
                message=f"Please provide collection name. {required_fields}, item: list."
            )
        json_data = kwargs.get("item")
        if not json_data:
            raise CreateException(
                message=f"Please provide data to create record. {required_fields}, item: list."
            )
        try:
            result = await MongoDBClient().db[collection_name].insert_many(json_data)
        except Exception as e:
            logger.exception(e)
            raise MongoDatabaseException(message="Unable to insert record.")
        return result

    @classmethod
    async def run_pipeline(cls, pipeline: list, **kwargs):
        """
        The run_pipeline function is a helper function that allows you to run an aggregation pipeline on the database.

        :param cls: Create an instance of the class
        :param pipeline: list: Pass the list of aggregation stages to be executed
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A list of dictionaries
        """
        collection_name = kwargs.get("collection_name")
        if not collection_name:
            raise CollectionNotProvidedException(
                message=f"Please provide collection name. {required_fields}, item: list."
            )
        pipeline = pipeline or []
        # pipeline.append({"$project": {"_id": 0}})
        try:
            responses = MongoDBClient().db[collection_name].aggregate(pipeline=pipeline)
            responses = await responses.to_list(length=MongoDBClient().fetch_max_len)
        except Exception as e:
            logger.exception(e)
            raise MongoDatabaseException(message="Unable to insert record.")
        return responses

    @classmethod
    async def delete(cls, **kwargs):
        """
        The delete function deletes a record from the database.
            Args:
                collection_name (str): The name of the collection to delete a record from.
                query (dict): A dictionary containing the query to identify the record(s) to be deleted.

        :param cls: Pass the class name of the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: A pymongo DeleteResult object that provides the status of the operation
        """
        collection_name = kwargs.get("collection_name")
        if not collection_name:
            raise CollectionNotProvidedException(
                message="Please provide a collection name."
            )
        query = kwargs.get("query")
        if not query:
            raise DeleteException(
                message="Please provide a query to delete record."
            )
        try:
            result = await MongoDBClient().db[collection_name].delete_one(query)
        except Exception as e:
            logger.exception(e)
            raise MongoDatabaseException(message="Unable to delete record.")
        return result
