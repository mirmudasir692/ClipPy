from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from typing import Optional, Union

from .config import set, get

MongoTarget = Union[MongoClient, Database]

def setup(
    mongo: Optional[MongoTarget] = None,
    uri: str = ""
):
    if mongo is not None:
        set("mongo", mongo)

    elif uri:
        client = MongoClient(uri)
        set("mongo", client)

    else:
        raise ValueError("Either mongo instance or uri must be provided")

    return get("mongo")
