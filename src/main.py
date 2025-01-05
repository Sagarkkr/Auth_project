from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
#Local imports
from src.db.mongo_init import MongoDBClient
from src.router import api_router_v1

app = FastAPI()
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    """
    The startup_event function is a coroutine that runs when the bot starts up.
    It initiates the database and registers all of our models with Flask-Admin.

    :return: A list of tasks to run when the server starts

    """
    await MongoDBClient.setup_mongodb(app)
    scheduler.start() 


@app.on_event("shutdown")
async def shutdown_event():
    await MongoDBClient.close_mongo_connection()
    scheduler.shutdown()

app.include_router(api_router_v1)