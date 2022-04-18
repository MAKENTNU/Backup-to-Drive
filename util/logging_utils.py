import logging.config

import settings


logging.config.dictConfig(settings.LOG_CONFIG)

logger = logging.getLogger(__name__)
