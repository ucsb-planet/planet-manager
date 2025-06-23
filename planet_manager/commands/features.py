from asyncio import run as aiorun

import typer
from planet import FeaturesClient

from planet_manager.session import session

app = typer.Typer()


pl = session()

async def __list():
    async with pl._session as sess:
        client = FeaturesClient(sess)

        collections = client.list_collections()
        async for collection in collections:
            print(collection)
            collection.__eq__

        # items = client.list_items(collection_id)
        # async for item in items:
            # print(items)
        #
async def __add():
    async with pl._session as sess:
        client = FeaturesClient(sess)
        collection = await client.create_collection(title="my collection", description="a new collection")
        # items = client.list_items(collection_id)
        # async for item in items:
            # print(items)

@app.command()
def list():
    aiorun(__list())

@app.command()
def add():
    aiorun(__add())
    # subscription = Subscription.load_by_id(id)
    # print(subscription_status(subscription, verbose))

# if __name__ == "__main__":
#     app()
# def main():
#     app()
