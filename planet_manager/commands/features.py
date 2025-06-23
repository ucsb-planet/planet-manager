from asyncio import run as aiorun

import geojson
import typer
from planet import FeaturesClient

from planet_manager.features import Features
from planet_manager.session import session

from planet_manager.utils import features_list
app = typer.Typer()


pl = session()


async def __list(collection_id: str):
    async with pl._session as sess:
        client = FeaturesClient(sess)

        features_json = client.list_items(collection_id)

        features_in = []
        async for feature_json in features_json:
            features_in.append(feature_json)

        features = Features.load(features_in)

        print(features_list(features))


async def __add(collection_id: str, geometry: dict, property_id: str):
    async with pl._session as sess:
        client = FeaturesClient(sess)

        await client.add_items(collection_id, geometry, property_id=property_id)


async def __delete(collection_id: str, feature_id: str):
    async with pl._session as sess:
        client = FeaturesClient(sess)

        await client.delete_item(collection_id, feature_id)


@app.command()
def list(collection_id: str):
    aiorun(__list(collection_id))


@app.command()
def add(collection_id: str, geojson_file: str):
    geometry = None

    if geojson_file:
        with open(geojson_file, "r") as file:
            geometry = geojson.load(file)

    aiorun(__add(collection_id, geometry, property_id="Name"))


@app.command()
def delete(collection_id: str, feature_id: str):
    aiorun(__delete(collection_id, feature_id))
