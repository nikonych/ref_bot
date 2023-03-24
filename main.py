import asyncio
import logging

from logs.logger_conf import setup_logging
from bot import main

logger = logging.getLogger()

logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

if __name__ == '__main__':
    try:
        setup_logging('logs/logger.yml')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
