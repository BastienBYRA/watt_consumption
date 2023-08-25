from datetime import datetime, timedelta
import docker
from docker.models.containers import Container
from docker import DockerClient
from time import sleep
import threading
from models.docker_cluster_template import DockerClusterTemplate
from utils.logger import Logger
from sys import exit

class DockerService:
    def __init__(self):
        self.__client: DockerClient | None = docker.from_env()
        self.network_name: str | None = self.create_default_network()
        self.list_container: list[Container] | None = []
        self.__logger: Logger | None = Logger("DOCKER_HELPER")
       
    def get_network(self):
        return self.network_name
       
    def check_container_running(self, container:Container):
        '''
        Check the given container is running, if not, try to rerun it
        
        If it can't, then stop all containers
        '''
        
        nb_try_to_load = 0
        while(True):
            container.reload() # reload to retrieve the last status

            # if "created" or "restarting", wait
            if container.status != 'running' and container.status != 'exited': 
                sleep(1)
                
            # if "exited", stop all containers and exit
            elif container.status == 'exited':
                self.__logger.log("Le container " + container.image.tags[0] + " n'arrive pas à se lancer \r\n", "red")
                self.__logger.log(repr(container.logs()), "red")
                self.kill_all_container()
                exit(-1)
            
            # if "running", try the next container 
            elif container.status == 'running':
                break

            # else, try to re-run it, if it doesn't work 3 times, stop all containers and exit
            else:
                nb_try_to_load = nb_try_to_load + 1
                if nb_try_to_load > 3:
                    self.__logger.log("N'arrive pas à lancer le container " + container.image.tags[0], "dark_grey")
                    self.kill_all_container()
                    exit(-1)
                container.start()
                    
        self.__logger.log(f"Le container \"{container.name}\" est en route.", "dark_grey")
        
        
        
         
    def run_all_docker_image(self, docker_cluster_template: DockerClusterTemplate):
        '''
        Run all the containers given by the user
        
        Args:
            docker_cluster_template (DockerClusterTemplate) : List of DockerContainerTemplate, containing the image name, arguments, ports and container name
            
        Returns:
            list[Container] : list of all the container instance of the specified DockerClusterTemplate
        '''
        
        self.__logger.log("Lancement des images docker en cours...", "dark_grey")
        
        try:  
            for docker_container_template in docker_cluster_template.list_docker_containers_templates:
                
                self.kill_container_based_on_name(docker_container_template.container_name)
                
                self.list_container.append(self.__client.containers.run(
                    docker_container_template.image_name,
                    detach=True,
                    tty=True,
                    environment=docker_container_template.arguments,
                    ports=docker_container_template.ports,
                    network=self.network_name,
                    name=docker_container_template.container_name,
                    ))

                # Some container may need time to load things here and there, truly a masterpiece of programming if you ask me
                sleep(5)
                # Really, i do things this is the best code i ever write.
                
                # Wait for the container to run
                self.check_container_running(self.list_container[-1])

                
        except:
            self.__logger.log("Impossible de lancer un des containers.", "red")
            self.kill_all_container()
            exit(404)
         
         
    def kill_container_based_on_name(self, name):
        '''Kill a container based on the name of the container'''
        
        try:
            container_to_delete = self.__client.containers.get(name)
            
            # if not found, go on except, otherwise
            self.__logger.log(f"Le container \"{name}\" existe déjà, suppression de celui existant.", "dark_grey")
            try:
                container_to_delete.remove()
            except:
                container_to_delete.remove(force=True)
            
        except:
            pass
        
    
    def get_CPU_and_RAM_usage(self, result: list, stop_event: threading.Event):
        '''
        Get the sum of the CPU and RAM % usage of all the containers
        '''
        
        sum_cpu_usage = 0
        
        self.__logger.log("Récupération de la consommation CPU et RAM des containers en cours...", "dark_grey")
        
        while not stop_event.is_set():
            sum_cpu_usage = 0
            
            for container in self.list_container:
                stats = container.stats(stream=False)
                
                cpu_stats = stats['cpu_stats']
                cpu_total_usage = cpu_stats['cpu_usage']['total_usage']
                cpu_system_usage = cpu_stats['system_cpu_usage']
                cpu_usage_percent = (cpu_total_usage / cpu_system_usage) * 100
                sum_cpu_usage+=cpu_usage_percent
                
                # memory_stats = stats['memory_stats']
                # memory_limit = memory_stats['limit']
                # memory_usage = memory_stats['usage']
                # ram_usage_percent = (memory_usage / memory_limit) * 100
                
                # ram_usage_percent+=ram_usage_percent
                
                ram_bit_usage = stats["memory_stats"]["usage"]
                
            result.append({
                # "t_mesure": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "t_mesure": (datetime.now() + timedelta(hours=2)).isoformat(),
                "cpu": sum_cpu_usage,
                "ram": ram_bit_usage,
            })

        return result


    def kill_all_container(self) -> None: 
        '''
        Stop and remove all container
        '''
        
        self.__logger.log("Suppression des containers en cours...", "dark_grey")
        
        for container in self.list_container:
            container_name = container.image.tags[0]
            container.stop()
            
            # Remove the container, force the removal of the container if it can't normally be removed
            try:
                container.remove()
            except:
                container.remove(force=True)
            self.__logger.log(container_name + " tué.", "dark_grey")


    def create_default_network(self) -> None:
        '''
        Create a default network to connect every container
        '''
        
        networks = self.__client.networks.list()
        network_name = "default-network"

        # Check if the network already exits
        already_has_network = False
        for network in networks:
            if network.name == network_name:
                already_has_network = True
                
        if already_has_network == False:
            self.__client.networks.create(network_name, driver="bridge")
            
        self.network_name = network_name
        
        
    def check_all_containers_running(self):
        '''
        Check that all containers is running, if not, try to rerun it, or stop all containers
        '''
        
        for container in self.list_container:
            nb_try_to_load = 0
            while(True):
                container.reload() # reload to retrieve the last status

                # if "created" or "restarting", wait
                if container.status != 'running' and container.status != 'exited': 
                    sleep(1)
                    
                # if "exited", stop all containers and exit
                elif container.status == 'exited':
                    self.__logger.log("Le container " + container.image.tags[0] + " n'arrive pas à se lancer \r\n", "red")
                    self.__logger.log(repr(container.logs()), "red")
                    # self.kill_all_container()
                    exit(-1)
                
                # if "running", try the next container 
                elif container.status == 'running':
                    break

                # else, try to re-run it, if it doesn't work 3 times, stop all containers and exit
                else:
                    nb_try_to_load = nb_try_to_load + 1
                    if nb_try_to_load > 3:
                        self.__logger.log("N'arrive pas à lancer le container " + container.image.tags[0], "dark_grey")
                        self.kill_all_container()
                        exit(-1)
                    container.start()
                    
        self.__logger.log("Tous les containers fonctionne !", "dark_grey")