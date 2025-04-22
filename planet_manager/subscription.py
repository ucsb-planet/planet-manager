from dataclasses import dataclass, field
from datetime import datetime

from dateutil.parser import parse
from planet.subscription_request import build_request, catalog_source, s3_compatible

from planet_manager.session import session

pl = session()


@dataclass
class CatalogSource:
    item_types: list[str] = field(default_factory=["PSScene"])
    asset_types: list[str] = field(
        default_factory=[
            "ortho_analytic_8b",
            "ortho_analytic_8b_sr",
            "ortho_analytic_8b_xml",
            "ortho_udm2",
        ]
    )
    geometry: list = field(default_factory=[])
    start_time: datetime = datetime(2000, 1, 1)
    filter: list[dict] | None = None
    end_time: datetime | None = None
    publishing_stages: list[str] = field(default_factory=["standard"])
    time_range_type: str = "published"

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
        end_time = input["parameters"].get("end_time", None)
        end_time = parse(end_time) if end_time else None

        return CatalogSource(
            item_types=input["parameters"]["item_types"],
            asset_types=input["parameters"]["asset_types"],
            geometry=input["parameters"]["geometry"],
            start_time=parse(input["parameters"]["start_time"]),
            end_time=end_time,
            publishing_stages=input["parameters"]["publishing_stages"],
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
    source: CatalogSource
    delivery: S3CompatibleDelivery
    created: datetime | None = None
    links: Links | None = None
    status: str | None = None
    id: str | None = None
    updated: datetime | None = None

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
        print(self.source.source)
        request = build_request(
            self.name, source=self.source.source, delivery=self.delivery.delivery
        )

        subscription = pl.subscriptions.create_subscription(request)
        #
        # self = Subscription.load(subscription)
        #
        # return self
