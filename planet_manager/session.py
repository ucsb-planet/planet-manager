from planet import Planet, Session
from planet.auth import APIKeyAuth

from planet_manager.config import config


def session():
    conf = config()

    pl = Planet(session=Session(auth=APIKeyAuth(key=conf.get("planet").get("api_key"))))
    return pl
