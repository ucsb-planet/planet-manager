from dataclasses import dataclass
from datetime import datetime

import planet
from dateutil.parser import parse
from planet.subscription_request import build_request, catalog_source, s3_compatible


class CatalogSource:
    def __init__(
        self,
        item_types=["PSScene"],
        asset_types=[
            "ortho_analytic_8b",
            "ortho_analytic_8b_sr",
            "ortho_analytic_8b_xml",
            "ortho_udm2",
        ],
        geometry=[],
        start_time=datetime(2000, 1, 1),
        filter=None,
        end_time: datetime | None = datetime(2026, 1, 31),
        publishing_stages="standard",
        time_range_type="published",
    ):
        self.__item_types = item_types
        self.__asset_types = asset_types
        self.__geometry = geometry
        self.__start_time = start_time
        self.__filter = filter
        self.__end_time = end_time
        self.__publishing_stages = publishing_stages
        self.__time_range_type = time_range_type

    @property
    def source(self):
        return catalog_source(
            self.__item_types,
            self.__asset_types,
            self.__geometry,
            self.__start_time,
            filter=self.__filter,
            end_time=self.__end_time,
            publishing_stages=self.__publishing_stages,
            time_range_type=self.__time_range_type,
        )

    def cancel(input: dict):
        pass

    @staticmethod
    def load(input: dict):
        end_time = input["parameters"].get("end_time", None)
        end_time = parse(end_time) if end_time else None

        return CatalogSource(
            input["parameters"]["item_types"],
            input["parameters"]["asset_types"],
            input["parameters"]["geometry"],
            parse(input["parameters"]["start_time"]),
            end_time,
            input["parameters"]["publishing_stages"],
        )


class S3CompatibleDelivery:
    def __init__(
        self,
        endpoint,
        bucket,
        region,
        access_key_id,
        secret_access_key,
        use_path_style=True,
    ):
        self.__endpoint = endpoint
        self.__bucket = bucket
        self.__region = region
        self.__access_key_id = access_key_id
        self.__secret_access_key = secret_access_key
        self.__use_path_style = use_path_style

    @property
    def delivery(self):
        return s3_compatible(
            self.__endpoint,
            self.__bucket,
            self.__region,
            self.__access_key_id,
            self.__secret_access_key,
            self.__use_path_style,
        )

    @staticmethod
    def load(input: dict):
        use_path_style = input["parameters"].get("use_path_style", None)

        return S3CompatibleDelivery(
            input["parameters"]["endpoint"],
            input["parameters"]["bucket"],
            input["parameters"]["region"],
            input["parameters"]["access_key_id"],
            input["parameters"]["secret_access_key"],
            use_path_style,
        )


class Links:
    def __init__(self, index, results):
        self.__index = index
        self.__results = results

    @staticmethod
    def load(input: dict):
        return Links(
            input["_self"],
            input["results"],
        )


@dataclass
class Subscription:
    name: str
    source: CatalogSource
    delivery: S3CompatibleDelivery
    created: datetime | None = None
    links: Links | None = None
    status: str | None = None
    id: str | None = None
    updated: datetime | None = None

    pl = planet.Planet()

    @staticmethod
    def load(input: dict):
        return Subscription(
            input["name"],
            CatalogSource.load(input["source"]),
            S3CompatibleDelivery.load(input["delivery"]),
            parse(input["created"]),
            Links.load(input["_links"]),
            input["status"],
            input["id"],
            parse(input["updated"]),
        )

    def subscribe(self):
        print(self.source.source)
        request = build_request(
            self.name, source=self.source.source, delivery=self.delivery.delivery
        )

        subscription = self.pl.subscriptions.create_subscription(request)
        #
        # self = Subscription.load(subscription)
        #
        # return self
