from dataclasses import dataclass

import logging


logger = logging.getLogger(__name__)


@dataclass
class DBConfig:
    type: str = None
    path: str = None

    @property
    def uri(self):
        url = f'{self.type}://{self.path}'
        logger.debug(url)
        return url
