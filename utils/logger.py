from datetime import datetime
from enum import Enum
from termcolor import colored

class Logger:
    def __init__(self, module_name: str):
        self.__module_name: str | None = module_name
    
    def now(self):
        '''Returns the current datetime'''
        return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    
    def log(self, message: str, color: str = "white"):
        '''Logs a message'''
        print(colored(message, color.lower()))
        
    def log_now(self, message: str, color: str = "white"):
        '''Logs a message with the current datetime and the module'''
        print(colored(f"{self.now()} - {self.__module_name} : {message}", color.lower()))