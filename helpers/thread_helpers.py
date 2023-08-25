import threading
from threading import Event
from threading import Thread
from typing import Callable

class ThreadHelper:
    def __init__(self):
        self.__list_thread: list[Thread] | None = []
        self.__thread_event: Event | None = None
        
    def start_thread(self, callable_function: Callable, object_that_will_recieve_value: object, event: Event, **kwargs):
        '''Start a new thread that will run a function'''
        thread = threading.Thread(target=callable_function, args=(object_that_will_recieve_value, event), kwargs=kwargs)
        self.__list_thread.append(thread)
        self.__thread_event = event
        thread.start()
        
        
    def trigger_signal_to_stop_all_threads_related_to_event(self):
        '''Block all threads related to the event'''
        self.__thread_event.set()
        
        
    def stop_all_thread(self):
        '''Stop all threads'''
        for thread in self.__list_thread:
            thread.join()
        
        self.__list_thread.clear()
        self.__thread_event.clear()
            