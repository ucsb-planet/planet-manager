import os
from datetime import datetime

import geojson
import typer

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
    subscriptions_list,
    extract_geometry,
    subscription_status,
)

pl = session()

app = typer.Typer()


@app.command()
def status(id: str):
    subscription = Subscription.load_by_id(id)
    print(subscription_status(subscription))


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
    name: str,
    geojson_file: str,
    start_time: str = "2000-01-01",
    end_time: str = "2026-02-01",
    time_range_type: str = "published",
):
    """
    Add a new subscription
    """

    with open(geojson_file, "r") as file:
        geojson_str = geojson.load(file)

    geometry = extract_geometry(geojson_str)

    start_time_obj = datetime.strptime(start_time, "%Y-%m-%d")
    end_time_obj = datetime.strptime(end_time, "%Y-%m-%d")

    source = CatalogSource(
        geometry=geometry,
        start_time=start_time_obj,
        filter=Filters.base_filter,
        end_time=end_time_obj,
        publishing_stages=["standard"],
        time_range_type=time_range_type,
    )

    conf = config()

    delivery = S3CompatibleDelivery(
        conf.get("endpoint"),
        conf.get("bucket"),
        conf.get("region"),
        conf.get("access_key_id"),
        conf.get("secret_access_key"),
        conf.get("use_style_path"),
    )

    subscription = Subscription(name, source, delivery)
    subscription.subscribe()


def main():
    app()
