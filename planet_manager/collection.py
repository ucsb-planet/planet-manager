from dataclasses import dataclass
from datetime import datetime

from dateutil.parser import parse


@dataclass
class Collection:
    title: str
    description: str
    item_type: str
    id: str | None = None
    created: datetime | None = None
    updated: datetime | None = None
    # links: Links | None = None
    feature_count: int | None = None
    area: int | None = None
    title_property: str | None = None
    description_property: str | None = None
    # permissions: dict | None = None
    # ownership: dict | None = None

    # @staticmethod
    # def load_by_id(id: str):
    #     subscription = pl.subscriptions.get_subscription(id)
    #
    #     return Subscription.load(subscription)
    #
    @staticmethod
    def load(input: dict):
        return Collection(
            input["title"],
            input["description"],
            input["item_type"],
            input["id"],
            parse(input["created"]),
            parse(input["updated"]),
            # Links.load(input["_links"]),
            input["feature_count"],
            input["area"],
            input["title_property"],
            input["description_property"],
            # input["permissions"],
            # input["ownership"],
        )

    #
    # def subscribe(self):
    #     request = build_request(
    #         self.name, source=self.source.source, delivery=self.delivery.delivery
    #     )
    #
    #     pl.subscriptions.create_subscription(request)
    #
    # def update(self):
    #     request = build_request(
    #         self.name, source=self.source.source, delivery=self.delivery.delivery
    #     )
    #
    #     pl.subscriptions.update_subscription(self.id, request)
