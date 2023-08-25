from datetime import datetime, timedelta
from threading import Event
from time import sleep
from utils.logger import Logger
from services.docker_services import DockerService
from helpers.thread_helpers import ThreadHelper
from models.Probe import Probe
from sys import exit

class DataCollectService:
    def __init__(self):
        self.__logger: Logger | None = Logger("COLLECT_DATA")
        self.__wattmetre : Probe | None = Probe()
        self.__thread_helper: ThreadHelper | None = ThreadHelper()
        self.__docker_helper: DockerService | None = DockerService()
        
        self.list_cpu_and_ram_stats = []
        self.list_watts_stats = []
        self.date_start: str | None = None
        self.date_end: str | None = None
     
        
    def start(self, docker_helper: DockerService, event: Event):
        '''Start all process of collecting data inside threads'''
       
        # Collect the watt consumption
        socket = self.__wattmetre.connect_socket()

        # if can't connect to the socket, kill the containers and stop program
        if socket == None:
            self.__docker_helper.kill_all_container()
            exit(1)
            
        else:
            # Collect the CPU and RAM usage info
            self.__thread_helper.start_thread(docker_helper.get_CPU_and_RAM_usage, self.list_cpu_and_ram_stats, event)
            
            # Collect the Watt consumption
            self.__thread_helper.start_thread(self.__wattmetre.collect_data, self.list_watts_stats, event, socket=socket)
            self.date_start = (datetime.now() + timedelta(hours=2)).isoformat() # start date
        
        
    def stop(self):
        '''Stop all the process of collecting data'''
        self.__thread_helper.trigger_signal_to_stop_all_threads_related_to_event()
        self.__thread_helper.stop_all_thread()
        self.date_end = (datetime.now() + timedelta(hours=2)).isoformat() # end date
    
    
    def collect(self, docker_helper: DockerService, event: Event, time_collect: int):
        '''Start collecting data and stop all the process of collecting after a specified amount of time'''
        
        self.start(docker_helper, event)
        
        sleep(time_collect)
        
        self.__logger.log("Fin de récupération des données !", "dark_grey")
        self.stop()
        