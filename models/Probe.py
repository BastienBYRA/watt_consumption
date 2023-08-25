from datetime import datetime, timedelta
import threading
import time
from enum import Enum
from multiprocessing import Queue, Pipe, Process
from multiprocessing.connection import Connection
from docker.models.containers import Container
from utils.logger import Logger
from models.sem6000 import SEMSocket


class MessageType(Enum):
    STOP_SIGNAL = 0,
    MEASURE = 1,
    START_OF_MEASUREMENT = 2,
    END_OF_MEASUREMENT = 3


class Probe:
    def __init__(self):
        self.__conn1: Connection | None = None
        self.__conn2: Connection | None = None
        self.__child_process: Process | None = None
        self.logger: Logger | None = Logger("WATTMETRE")

    def connect_socket(self) -> SEMSocket | None:
        '''Connect to the socket

        Returns a SEMSocket object or None if the socket isn't found nor connected'''

        # Get the socket
        try:
            IP_SOCKET = "DEFINE YOUR SOCKET IP HERE"

            if IP_SOCKET == "DEFINE YOUR SOCKET IP HERE":
                self.logger.log(
                    "Veuillez définir l'adresse IP du Wattmètre dans le fichier models\Probe.py", "red")
                return None

            socket = SEMSocket(IP_SOCKET)
        except:
            self.logger.log("Impossible de trouver le Wattmètre...", "red")
            return None

        # Try to connect to the socket 5 times, if failed 5, then stop everything
        number_try_connect_socket = 0
        while True:
            if not socket.login("0000") or not socket.connected:
                if number_try_connect_socket < 5:
                    self.logger.log(
                        "Echec de la connexion au Wattmètre...", "light_red")
                    number_try_connect_socket += 1
                    time.sleep(3)
                else:
                    self.logger.log(
                        "Impossible de se connecter au Wattmètre...", "red")
                    return None
            else:
                return socket

    def collect_data(self, result: list, stop_event: threading.Event, socket: SEMSocket):
        __logger: Logger | None = Logger("PROBE")
        __logger.log(
            "Récupération de la consommation en Watt en cours...", "dark_grey")

        try:
            while not stop_event.is_set():
                socket.getStatus()
                result.append({
                    "t_mesure": (datetime.now() + timedelta(hours=2)).isoformat(),
                    "watt": socket.power
                })
        finally:
            socket.disconnect()
        return result


# if __name__ == "__main__":
#     p = Probe()
#     p.start_measurement()
#     time.sleep(10)
#     p.end_measurement()
