import motor.motor_asyncio

from src.core.config import settings
from src.core.logger_config import logger


class MongoDBClient:
    _instance = None
    _client = None
    _db = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                # mongo_conf: str = (
                #     f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@{settings.MONGO_HOST}/"
                # )
                mongo_conf: str = "mongodb+srv://Sagar2022:Kripa2022@authcluster.dt9ei.mongodb.net/"
                cls._instance._client = motor.motor_asyncio.AsyncIOMotorClient(mongo_conf)
                cls._instance._db = cls._instance._client[settings.MONGO_DATABASE]
                logger.info("Connected to MongoDB.")
            except Exception as e:
                logger.exception(f"Error connecting to MongoDB: {e}")
        return cls._instance

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db

    @property
    def fetch_max_len(self):
        return 250

    @classmethod
    async def get_collection(cls, collection_name: str):
        return cls._db[collection_name]

    @classmethod
    async def setup_mongodb(cls, app):
        """
        Helper function to set up MongoDB connection & `motor` client during setup.
        Use during app startup as follows:

        .. code-block:: python

            app = FastAPI()

            @app.on_event('startup')
            async def startup():
                setup_mongodb(app)

        Args:
            app: app object, instance of FastAPI

        Returns:
            None
        """
        mongo_obj = MongoDBClient()
        app.mongodb_client = mongo_obj.client

    @classmethod
    async def close_mongo_connection(cls):
        """
        Helper function to close MongoDB connection.
        """
        mongo_obj = MongoDBClient()
        mongo_obj.client.close()
        logger.info("MongoDB connection closed.")
# mongodb+srv://Sagar2022:Kripa2022@authcluster.dt9ei.mongodb.net/