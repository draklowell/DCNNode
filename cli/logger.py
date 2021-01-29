from colors import color

from .console import Console
from datetime import datetime

INFO = [{}, "INFO"]
WARNING = [{"fg": "yellow"}, "WARNING"]
ERROR = [{"fg": "red"}, "ERROR"]
CRITICAL = [{"fg": "white", "bg": "red", "style": "bold"}, "CRITICAL"]


class Logger:
    def __init__(self, console: Console, debug_file, date_format: str = "%Y-%m-%d %H:%M:%S", level="", parent=None):
        self.date_format = date_format
        self.console = console
        self.level = level
        self.parent = parent
        self.show_prefix = True
        self.debug_file = debug_file
        self.debug_file.write(f"BEGIN OF LOG AT {datetime.now().strftime(self.date_format)}\n")

    def isRoot(self):
        return self.parent is None

    def getRoot(self):
        if self.isRoot():
            return self
        else:
            return self.parent.getRoot()

    def getParent(self):
        return self.parent

    def create(self, level):
        return Logger(self.console, self.debug_file, self.date_format, level, self)

    def togglePrefix(self, status=True):
        self.show_prefix = status

    def getPrefix(self):
        if self.show_prefix:
            if self.isRoot():
                return datetime.now().strftime(self.date_format)
            else:
                return self.getParent().getPrefix() + " " + self.level
        else:
            return ""

    def log(self, level=INFO, text=""):
        prefix = self.getPrefix()
        prefix = f"[{prefix}] " if prefix else prefix
        self.debug_file.write(f"[{level[1]}]" + prefix + str(text) + "\n")
        self.console.print( color(prefix + str(text), **level[0]))

    def info(self, text=""):
        self.log(INFO, text)

    def warning(self, text=""):
        self.log(WARNING, text)

    def error(self, text=""):
        self.log(ERROR, text)

    def critical(self, text=""):
        self.log(CRITICAL, text)
