from planet_manager.subscriptions import Subscriptions
from planet_manager.subscription import Subscription

from colorama import Fore, Style

from planet_manager.collections import Collections
from planet_manager.features import Features


def extract_geometry(data: dict) -> dict:
    if "features" in data and data["features"]:
        return data["features"][0]["geometry"]
    elif "geometry" in data:
        return data["geometry"]
    else:
        return data


def subscriptions_list(subscriptions: Subscriptions):
    out = f"{'ID':<36} | {'Created':<19} | {'Status':<10} | Name\n{'-' * 120}\n"

    for subscription in subscriptions:
        out += f"{Style.RESET_ALL + subscription.id:<36} {Style.RESET_ALL + '|'} {
            Fore.LIGHTBLUE_EX
            + subscription.created.strftime('%Y-%m-%d %H:%M:%S'):<19} {
            Style.RESET_ALL + '|'
        } {Fore.LIGHTMAGENTA_EX + subscription.status:<15} {Style.RESET_ALL + '|'} {
            Fore.GREEN + subscription.name:<10}\n"

    return out


def subscription_status(subscription: Subscription, verbose: bool = False):
    out = f"""name:                  {subscription.name}
id:                    {subscription.id}
status:                {subscription.status}
created:               {subscription.created}
updated:               {subscription.updated}
{Fore.LIGHTBLUE_EX}source:
    item_types:        {subscription.source.item_types}
    asset_types:       {subscription.source.asset_types}
    geometry:          {
        subscription.source.geometry if verbose else "<REDACTED, use --verbose>"
    }
    start_time:        {subscription.source.start_time}
    filter:            {subscription.source.filter}
    end_time:          {subscription.source.end_time}
    publishing_stages: {subscription.source.publishing_stages}
    time_range_type:   {subscription.source.time_range_type}
    rrule:             {subscription.source.rrule}
{Fore.GREEN}delivery:
    endpoint:          {subscription.delivery.endpoint}
    bucket:            {subscription.delivery.bucket}
    region:            {subscription.delivery.region}
    access_key_id:     {subscription.delivery.access_key_id}
    secret_access_key: {subscription.delivery.secret_access_key}
    use_path_style:    {subscription.delivery.use_path_style}
{Fore.LIGHTMAGENTA_EX}links:
    _self:             {subscription.links.index}
    results:           {subscription.links.results}
"""
    return out


def collections_list(collections: Collections):
    out = f"{'ID':<36} | {'Description':<35} | Created\n{'-' * 120}\n"

    for collection in collections:
        out += f"{Style.RESET_ALL + collection.id:<40} {Style.RESET_ALL + '|'} {
            Fore.LIGHTMAGENTA_EX + collection.description:<40} {
            Style.RESET_ALL + '|'
        }  {Fore.LIGHTBLUE_EX + collection.created.strftime('%Y-%m-%d %H:%M:%S'):<20}\n"

    return out

def features_list(features: Features):
    out = f"{'ID'}\n{'-' * 40}\n"

    for feature in features:
        out += f"{Style.RESET_ALL + feature.id}\n"

    return out
