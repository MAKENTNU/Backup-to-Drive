import logging.config
from typing import Final

import settings


logging.config.dictConfig(settings.LOG_CONFIG)

logger: Final = logging.getLogger(__name__)
