import time
import socket
import threading
import ssl
import requests

from .info import SSL_VERSION, HOSTLIST_ADDRESS
from .handler import Handler

class Server:
    def __init__(self, address: tuple, friendly_hosts: list, logger):
        self.address = address
        self.hosts = list(friendly_hosts)
        self.handler = Handler
        self.logger = logger.create("SERVER")
        self.handlers = []
        self.hashlist = {}
        self.offhandlers = []
        self.running = False
        try:
            self.socket = ssl.wrap_socket(
                socket.socket(),
                ssl_version=SSL_VERSION,
                server_side=True,
                cert_reqs=ssl.CERT_OPTIONAL,
                certfile="certificate/cert.crt",
                keyfile="certificate/key.pem"
            )
            self.socket.bind(address)
            self.socket.listen()
            self.socket.settimeout(0.1)
            self.logger.info(f"Server started on {self.address[0]}:{self.address[1]}")
        except Exception as e:
            self.logger.critical(f"Error when starting server: {e}")
            exit()
        
        for host in friendly_hosts:
            localLogger = self.logger.create(f"{host[0]}:{host[1]}")
            try:
                handler = self.handler.connect(host, localLogger, self, reconnect=True)
                handler.start()
                self.handlers.append(handler)
            except Exception as e: 
                localLogger.error(f"Error when connecting: {e}")

    def broadcast(self, packet: bytes):
        for i in self.handlers:
            i.send(packet)

    def _checkforever(self):
        last_check = 0
        while self.running:
            for i in self.handlers:
                if not i.alive:
                    self.handlers.remove(i)
            for h, t in reversed(self.hashlist.items()):
                if time.time() - t > 60*60*24:
                    del self.hashlist[h]
                else:
                    break
            if (not HOSTLIST_ADDRESS is None) and (time.time() - last_check > 5):
                last_check = time.time()
                try:
                    conn = requests.get(HOSTLIST_ADDRESS)
                    data = conn.json()
                    for i in data:
                        if i in self.offhandlers:
                            continue
                        try:
                            handler = self.handler.connect(i, self, reconnect=True)
                            handler.start()
                            self.handlers.append(handler)
                            self.offhandlers.append(i)
                        except Exception as e: 
                            pass
                except:
                    pass
            time.sleep(0.1)

    def serveforever(self):
        self.running = True
        threading.Thread(target=self._checkforever).start()
        while self.running:
            try:
                fd, addr = self.socket.accept()
                localLogger = self.logger.create(f"{addr[0]}:{addr[1]}")
                try:
                    handler = self.handler.handle(fd, addr, localLogger, self, reconnect=False)
                    handler.start()
                    self.handlers.append(handler)
                except Exception as e:
                    localLogger.error(f"Error when handling: {e}")
            except (socket.timeout, ssl.SSLError, OSError) :
                continue

    def close(self):
        self.running = False
        time.sleep(0.2)
        for i in self.handlers:
            i.close()
        self.socket.close()