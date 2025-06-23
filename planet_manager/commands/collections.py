from asyncio import run as aiorun

import typer
from planet import FeaturesClient

from planet_manager.session import session

from planet_manager.collections import Collections

from planet_manager.utils import collections_list

app = typer.Typer()


pl = session()


async def __list():
    async with pl._session as sess:
        client = FeaturesClient(sess)

        collections_json = client.list_collections()

        collections_in = []

        async for collection_json in collections_json:
            collections_in.append(collection_json)

        # print(collections_in)
        collections = Collections.load(collections_in)

        print(collections_list(collections))


async def __add(title: str, description: str):
    async with pl._session as sess:
        client = FeaturesClient(sess)
        collection = await client.create_collection(
            title=title, description=description
        )


async def __delete(id: str):
    async with pl._session as sess:
        client = FeaturesClient(sess)
        collection = await client.delete_collection(id)


@app.command()
def list():
    aiorun(__list())


@app.command()
def add(title: str, description: str):
    aiorun(__add(title, description))


@app.command()
def delete(id: str):
    aiorun(__delete(id))
