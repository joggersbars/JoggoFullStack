import logging
import os

def set_logging():
    is_debugled_enabled = os.getenv("DEBUG","").lower() == "true"
    log_level = logging.DEBUG if is_debugled_enabled else logging.INFO

    logging.basicConfig(level=log_level,
                        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s')

set_logging()