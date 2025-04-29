from dataclasses import dataclass, field
from datetime import datetime

from dateutil.parser import parse
from planet.subscription_request import build_request, catalog_source, s3_compatible

from planet_manager.session import session

pl = session()


@dataclass
class CatalogSource:
    item_types: list[str]
    asset_types: list[str]
    geometry: list | None
    start_time: datetime | None
    filter: list[dict] | None
    end_time: str | None
    publishing_stages: list[str] | None
    time_range_type: str | None

    @property
    def source(self):
        return catalog_source(
            self.item_types,
            self.asset_types,
            self.geometry,
            self.start_time,
            filter=self.filter,
            end_time=self.end_time,
            publishing_stages=self.publishing_stages,
            time_range_type=self.time_range_type,
        )

    def cancel(input: dict):
        pass

    @staticmethod
    def load(input: dict):
        # end_time = input["parameters"].get("end_time", None)
        # end_time = parse(end_time) if end_time else None

        return CatalogSource(
            item_types=input["parameters"]["item_types"],
            asset_types=input["parameters"]["asset_types"],
            geometry=input["parameters"]["geometry"],
            start_time=input["parameters"].get("start_time", None),
            filter=input["parameters"].get("filter", None),
            end_time=input["parameters"].get("end_time", None),
            publishing_stages=input["parameters"]["publishing_stages"],
            time_range_type=input["parameters"]["time_range_type"],
        )


@dataclass
class S3CompatibleDelivery:
    endpoint: str
    bucket: str
    region: str
    access_key_id: str
    secret_access_key: str
    use_path_style: bool

    @property
    def delivery(self):
        return s3_compatible(
            self.endpoint,
            self.bucket,
            self.region,
            self.access_key_id,
            self.secret_access_key,
            self.use_path_style,
        )

    @staticmethod
    def load(input: dict):
        use_path_style = input["parameters"].get("use_path_style", False)

        return S3CompatibleDelivery(
            input["parameters"]["endpoint"],
            input["parameters"]["bucket"],
            input["parameters"]["region"],
            input["parameters"]["access_key_id"],
            input["parameters"]["secret_access_key"],
            use_path_style,
        )


@dataclass
class Links:
    index: str
    results: str

    @staticmethod
    def load(input: dict):
        return Links(
            input["_self"],
            input["results"],
        )


@dataclass
class Subscription:
    name: str
    _source: CatalogSource
    _delivery: S3CompatibleDelivery
    created: datetime | None = None
    links: Links | None = None
    status: str | None = None
    id: str | None = None
    updated: datetime | None = None

    @property
    def delivery(self) -> str:
        return self._delivery

    @delivery.setter
    def delivery(self, v: S3CompatibleDelivery) -> None:
        for key, value in vars(v).items():
            if value:
                self.delivery.__setattr__(key, value)

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, v: CatalogSource) -> None:
        for key, value in vars(v).items():
            if value:
                self.source.__setattr__(key, value)

    @staticmethod
    def load_by_id(id: str):
        subscription = pl.subscriptions.get_subscription(id)

        return Subscription.load(subscription)

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
        request = build_request(
            self.name, source=self.source.source, delivery=self.delivery.delivery
        )

        pl.subscriptions.create_subscription(request)

    def update(self):
        request = build_request(
            self.name, source=self.source.source, delivery=self.delivery.delivery
        )

        pl.subscriptions.update_subscription(self.id, request)

