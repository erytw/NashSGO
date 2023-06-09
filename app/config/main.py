import logging.config

import yaml

from app.models.config.db import DBConfig
from app.models.config import Config
from app.models.config.main import Paths, BotConfig, BotApiConfig, BotApiType

logger = logging.getLogger(__name__)


def load_config(paths: Paths) -> Config:
    with (paths.config_path / "config.yaml").open("r") as f:
        config_dct = yaml.safe_load(f)

    return Config(
        paths=paths,
        db=load_db_config(config_dct["db"]),
        bot=load_bot_config(config_dct["bot"]),
    )


def load_db_config(db_dict: dict) -> DBConfig:
    return DBConfig(
        type=db_dict.get('type', None),
        path=db_dict.get('path', None),
    )


def load_bot_config(dct: dict) -> BotConfig:
    return BotConfig(
        token=dct["token"],
        log_chat=dct["log_chat"],
        bot_api=load_botapi(dct["botapi"])
    )


def load_botapi(dct: dict) -> BotApiConfig:
    return BotApiConfig(
        type=BotApiType[dct["type"]],
        botapi_url=dct.get("botapi_url", None),
        botapi_file_url=dct.get("file_url", None),
    )
