import threading
import base64
import socket
import time
import ssl

from .info import SSL_VERSION
from .packet import Packet

class Handler(threading.Thread):
    @classmethod
    def handle(cls, socket: socket.socket, address: tuple, logger, server, reconnect: bool = False):
        self = cls()
        self.logger = logger
        self.socket = socket
        self.socket.settimeout(0.1)
        self.address = address
        self.reconnect = reconnect
        self.server = server
        self.running = False
        self.connected = True
        return self

    @classmethod
    def connect(cls, address: tuple, logger, server, reconnect: bool = True):
        self = cls()
        self.logger = logger
        self.address = address
        self.reconnect = reconnect
        self.server = server
        self.running = False
        self.connected = True
        try:
            self.tryConnect()
        except (OSError, ssl.SSLError) as e:
            if self.reconnect:
                pass
            else:
                raise e
        return self
        
    def receive(self, packet: bytes):
        try:
            packet = Packet.fromPacked(packet)
            if packet.getHash() in self.server.hashlist:
                return
            self.server.hashlist[packet.getHash()] = time.time()
            packed = packet.getPacked()
            self.server.broadcast(int.to_bytes(len(packed), 2, "big") + packed)
            self.logger.info(f"New packet handled: {base64.b64encode(packet.getHash()).decode('utf-8')}")
        except Exception as e:
            self.logger.error(f"Packet handling failed with error: {e}")

    def send(self, packet: bytes):
        if self.alive:
            try:
                self.socket.send(packet)
            except Exception:
                self.logger.error(f"Failed to send packet")
 
    def tryConnect(self):
        self.socket = socket.socket()
        self.socket.settimeout(2)
        self.socket.connect(self.address)
        self.socket.settimeout(0.1)
        self.socket = ssl.wrap_socket(
            self.socket,
            ssl_version=SSL_VERSION,
            server_side=False,
            cert_reqs=ssl.CERT_NONE
        )

    def onDisconnected(self):
        if not self.reconnect:
            self.running = False
            self.connected = False
        else:
            try:
                self.tryConnect()
                self.logger.info(f"Successful reconnected")
            except (ConnectionError, ssl.SSLError, socket.timeout):
                pass

    def run(self):
        self.logger.info("Connection successful handled")
        self.running = True
        while self.running:
            try:
                packet_size = self.socket.recv(2)
            except (socket.timeout, ssl.SSLError, OSError):
                continue
            except OSError:
                self.onDisconnected()
                continue

            if packet_size == b"":
                self.logger.error(f"Connection lost")
                self.onDisconnected()
                continue

            packet_size = int.from_bytes(packet_size, "big")
            packet = self.socket.recv(packet_size)
            if packet == b"":
                self.logger.error(f"Connection lost")
                self.onDisconnected()
                continue
            self.receive(packet)

    def close(self):
        self.reconnect = False
        if self.running:
            self.running = False
        time.sleep(0.2)
        if self.alive:
            self.socket.close()

    @property
    def alive(self) -> bool:
        if self.reconnect:
            return True
        return self.connected