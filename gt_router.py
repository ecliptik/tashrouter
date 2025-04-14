import logging
import time
import signal
import sys
from collections import Counter

import tashrouter.netlog
from tashrouter.port.ethertalk.tap import TapPort
from tashrouter.port.localtalk.ltoudp import LtoudpPort
from tashrouter.port.localtalk.tashtalk import TashTalkPort
from tashrouter.router.router import Router

packet_drop_reasons = Counter()

def drop_packet(reason, datagram):
    packet_drop_reasons[reason] += 1
    logging.info(f"DROP: {reason}. Datagram: {datagram}")

def sigterm_handler(_signo, _stack_frame):
    logging.info("SIGTERM received. Shutting down...")
    sys.exit(0)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
)
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

if entry is None:
    logging.warning(f"No routing table entry found for destination network: {datagram.destination_network}")
    if datagram.destination_network == 0x0000:
        logging.info(f"DROP: Invalid destination network (0x0000) for Datagram: {datagram}")
    elif datagram.hop_count >= 15:
        logging.info(f"DROP: Exceeded maximum hop count for Datagram: {datagram}")
    elif not routing_table.get(datagram.destination_network):
        logging.warning(f"DROP: No routing table entry for destination network: {datagram.destination_network}. Datagram: {datagram}")
    else:
        logging.info(f"DROP: Packet dropped for unknown reason: {datagram}")
        logging.warning(f"Packet not processed on port {self.port_name}. Datagram: {datagram}")

if not is_valid_network(datagram.destination_network):
    logging.warning(f"Invalid destination network: {datagram.destination_network} for Datagram: {datagram}")
