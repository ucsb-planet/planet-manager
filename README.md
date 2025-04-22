# Planet Manager

A wrapper around the planet.com subscription API.

The goal of this project is to provide user friendly CLI for the subscriptions API. It is written specifically for the [Earth Research Institute](https://www.eri.ucsb.edu/), and may not satisfy all use cases. If you have a feature request, please submit an issue, or better yet, a pull request!

## Installation

`pip install planet_manager`

## Configuration

The configuration file is located at `$XDG_CONFIG_HOME/pman/config.toml`, following the [XDG Base Directory Spceification](https://specifications.freedesktop.org/basedir-spec/latest/)

An example configuration file:

```toml
[planet]
api_key = "MY_PLANET_API_KEY"

[object_storage]
# The endpoint can be any S3 compatible storage
endpoint = "https://my.s3.compatible.endpoint.url"
bucket = "planetdata"
region = "us-west-1"
access_key_id = "MY_ACCESS_KEY_ID"
secret_access_key = "MY_SECRET_ACCESS_KEY"
use_path_style = true
```

## Usage

### Add a subscription

`pman add NAME GEOJSON_FILE`

**NAME** a descriptive name for your AOI

**GEOJSON_FILE** that adheres to the [Planet GeoJSON Specifications](https://developers.planet.com/docs/planetschool/geojson-and-areas-of-interest-aois/#planet-geojson-specifications)


#### Example

![alt text](https://raw.githubusercontent.com/ucsb-planet/planet-manager/refs/heads/main/images/pman_add.png)

<hr/>

### List all subscriptions

`pman list`

#### Example

![alt text](https://raw.githubusercontent.com/ucsb-planet/planet-manager/refs/heads/main/images/pman_list.png)

<hr/>

### Get subscription status

`pman status ID`

#### Example

![alt text](https://raw.githubusercontent.com/ucsb-planet/planet-manager/refs/heads/main/images/pman_status.png)

<hr/>

### Cancel a subscription

`pman cancel ID`

#### Example

![alt text](https://raw.githubusercontent.com/ucsb-planet/planet-manager/refs/heads/main/images/pman_cancel.png)

<hr/>
