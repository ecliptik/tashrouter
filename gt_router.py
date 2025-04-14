import logging
import time
import signal
import sys

import tashrouter.netlog
from tashrouter.port.ethertalk.tap import TapPort
from tashrouter.port.localtalk.ltoudp import LtoudpPort
from tashrouter.port.localtalk.tashtalk import TashTalkPort
from tashrouter.router.router import Router

def sigterm_handler(_signo, _stack_frame):
    logging.info("SIGTERM received. Shutting down...")
    sys.exit(0)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
tashrouter.netlog.set_log_str_func(logging.debug)  # comment this line for speed and reduced spam

router = Router('router', ports=(
    LtoudpPort(seed_network=71, seed_zone_name=b'Vermilion Sands LT'),
    TashTalkPort(serial_port='/dev/ttyAMA0', seed_network=72, seed_zone_name=b'Vermilion Sands LT'),
    TapPort(tap_name='tap2', hw_addr=b'\xDE\xAD\xBE\xEF\xCA\xFE'),
))

logging.info("Initializing router with the following ports:")
for port in router.ports:
    logging.info(f"Port: {port.__class__.__name__}, Config: {port}")

logging.info("Starting the router...")
router.start()
logging.info("Router started successfully.")

signal.signal(signal.SIGTERM, sigterm_handler)

try:
    while True:
        logging.debug("Router is running...")
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    logging.info("Shutdown initiated.")
    router.stop()
    logging.info("Router stopped successfully.")
except Exception as e:
    logging.error(f"Unexpected error: {e}", exc_info=True)
    router.stop()
