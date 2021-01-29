from dcn.server import Server
from dcn.handler import Handler
from cli.console import Console
from cli.logger import Logger

from config import config
from dcn.info import VERSION

console = Console()
logger = Logger(console, open(config["DEBUG"]["FILE"], "a"), config["DEBUG"]["TIMEFORMAT"])
logger.togglePrefix(False)
logger.info(f"DCN Node [Ver. {VERSION}] by DrakLowell ( t.me/draklowellinfo )")
logger.info("Apache License 2.0")
logger.info()
logger.togglePrefix(True)

server = Server(config["ADDRESS"], config["FRIENDLY_HOSTS"], logger)
try:
    server.serveforever()
except KeyboardInterrupt:
    console.close()
    server.close()