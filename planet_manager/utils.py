import json


def extract_geometry(data: dict) -> dict:
        if "features" in data and data["features"]:
            return data["features"][0]["geometry"]
        elif "geometry" in data:
            return data["geometry"]
        else:
            return data
