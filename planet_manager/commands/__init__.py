import asyncio
import os
from datetime import datetime

import geojson
import typer
from planet import FeaturesClient

from planet_manager.commands import collections, features
from planet_manager.config import config
from planet_manager.filters import Filters
from planet_manager.session import session
from planet_manager.subscription import (
    CatalogSource,
    S3CompatibleDelivery,
    Subscription,
)
from planet_manager.subscriptions import Subscriptions
from planet_manager.utils import (
    extract_geometry,
    subscription_status,
    subscriptions_list,
)

pl = session()

app = typer.Typer()
app.add_typer(collections.app, name="collections")
app.add_typer(features.app, name="features")

asset_types = [
    "basic_analytic_4b",
    "basic_analytic_8b",
    "basic_analytic_8b_xml",
    "basic_analytic_4b_rpc",
    "basic_analytic_4b_xml",
    "basic_udm2",
    "ortho_analytic_3b",
    "ortho_analytic_3b_xml",
    "ortho_analytic_4b",
    "ortho_analytic_4b_sr",
    "ortho_analytic_4b_xml",
    "ortho_analytic_8b",
    "ortho_analytic_8b_sr",
    "ortho_analytic_8b_xml",
    "ortho_udm2",
    "ortho_visual",
]


@app.command()
def status(id: str, verbose: bool = False):
    subscription = Subscription.load_by_id(id)
    print(subscription_status(subscription, verbose))


@app.command()
def list(cancelled: bool = False):
    """
    List all subscriptions
    """
    subscriptions_json = pl.subscriptions.list_subscriptions()

    subscriptions = Subscriptions.load(subscriptions_json)

    if not cancelled:
        subscriptions = filter(lambda x: x.status != "cancelled", subscriptions)

    print(subscriptions_list(subscriptions))


@app.command()
def cancel(id: str):
    """
    Cancel a subscription
    """
    pl.subscriptions.cancel_subscription(id)


@app.command()
def add(
    geojson_file: str,
    name: str | None = None,
    start_time: str = "2000-01-01",
    end_time: str = "2026-02-01",
    rrule: str = "FREQ=MONTHLY;BYMONTH=1,2,3,4,5,6,7,8,9,10,11,12",
    time_range_type: str = "published",
):
    """
    Add a new subscription
    """

    with open(geojson_file, "r") as file:
        geojson_str = geojson.load(file)

    geometry = extract_geometry(geojson_str)
    name = name if name else geojson_str["properties"]["Name"]

    source = CatalogSource(
        item_types=["PSScene"],
        asset_types=asset_types,
        geometry=geometry,
        start_time=datetime.strptime(start_time, "%Y-%m-%d"),
        filter=Filters.base_filter,
        end_time=datetime.strptime(end_time, "%Y-%m-%d"),
        rrule=rrule,
        publishing_stages=["standard", "finalized"],
        time_range_type=time_range_type,
    )

    obj_conf = config().get("object_storage")

    delivery = S3CompatibleDelivery(
        obj_conf.get("endpoint"),
        obj_conf.get("bucket"),
        obj_conf.get("region"),
        obj_conf.get("access_key_id"),
        obj_conf.get("secret_access_key"),
        obj_conf.get("use_path_style"),
    )

    subscription = Subscription(name, source, delivery)

    subscription.subscribe()


@app.command()
def update(
    id: str,
    name: str | None = None,
    geojson_file: str | None = None,
    start_time: str = "2000-01-01",
    end_time: str = "2026-02-01",
    rrule: str = "FREQ=MONTHLY;BYMONTH=1,2,3,4,5,6,7,8,9,10,11,12",
    time_range_type: str = "published",
):
    """
    Update subscription
    """
    subscription = Subscription.load_by_id(id)

    if name:
        subscription.name = name

    obj_conf = config().get("object_storage")

    delivery = S3CompatibleDelivery(
        obj_conf.get("endpoint"),
        obj_conf.get("bucket"),
        obj_conf.get("region"),
        obj_conf.get("access_key_id"),
        obj_conf.get("secret_access_key"),
        obj_conf.get("use_path_style"),
    )
    subscription.delivery = delivery

    geometry = None
    if geojson_file:
        with open(geojson_file, "r") as file:
            geojson_str = geojson.load(file)

        geometry = extract_geometry(geojson_str)

    source = CatalogSource(
        item_types=["PSScene"],
        asset_types=asset_types,
        geometry=geometry,
        start_time=datetime.strptime(start_time, "%Y-%m-%d"),
        filter=Filters.base_filter,
        end_time=datetime.strptime(end_time, "%Y-%m-%d"),
        rrule=rrule,
        publishing_stages=["standard", "finalized"],
        time_range_type=time_range_type,
    )
    subscription.source = source

    subscription.update()


async def _features():
    async with pl._session as sess:
        client = FeaturesClient(sess)
        collection = await client.create_collection(
            title="my collection", description="a new collection"
        )
        items = client.list_items(collection_id)
        async for item in items:
            print(items)


@app.command()
def features():
    aiorun(_features())
    # subscription = Subscription.load_by_id(id)
    # print(subscription_status(subscription, verbose))


def main():
    app()
