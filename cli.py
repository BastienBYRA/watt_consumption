from datetime import datetime
from time import sleep
from models.docker_container_template import DockerContainerTemplate
from models.docker_cluster_template import DockerClusterTemplate
from _data.default_docker_cluster import DefaultDockerCluster
from utils.argument_utils import ArgumentUtils
from helpers.http_helpers import HTTPHelper
from utils.logger import Logger
from utils.cli_utils import CLIUtils
from models.report import Report
from sys import exit


class CLI:
    def __init__(self):
        self.report_name: str | None = None

        self.docker_cluster_template: DockerClusterTemplate | None = DockerClusterTemplate()
        self.docker_container_template: DockerContainerTemplate | None = DockerContainerTemplate()
        self.list_default_docker_cluster: DefaultDockerCluster = DefaultDockerCluster()

        self.http_helper: HTTPHelper | None = None
        self.duration_collect_data: int | None = None
        self.__cli_utils: CLIUtils | None = CLIUtils()
        self.__logger: Logger | None = Logger("CLI_APP")
        self.__arguments_utils: ArgumentUtils | None = ArgumentUtils()

    def init_HTTPHelper(self, http_helper: HTTPHelper):
        '''Initialize the HTTP helper'''
        self.http_helper = http_helper

    def get_name_for_report(self):
        '''Ask the user to give a name for the report'''
        report_name = input(
            "Veuillez saisir le nom du rapport (si vide, un nom par defaut sera donnés) : ")
        if report_name is None or report_name == "":
            report_name = f"report-stack-{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}"
            self.__logger.log(f"> {report_name}", "dark_grey")
        self.report_name = report_name

    def get_duration_collect_data(self) -> bool:
        '''Ask the user how many seconds do we retrieve data from the cluster'''

        time = input(
            "Pendant combien de temps voulez-vous collecter des données (en seconde) : ")
        if time.isnumeric() == True and time != None and time != "":
            self.duration_collect_data = int(time)
            return True
        else:
            return False

    def get_image_name(self):
        '''Ask the user to give the image name to run the container'''

        while True:
            docker_image_name = input(
                "Veuillez choisir une image Docker à lancer : ")
            if docker_image_name != "" and docker_image_name != None:
                break
        self.docker_container_template.set_image_name(docker_image_name)

    def get_arguments(self):
        '''Ask the user to give all the arguments required to run the container'''

        dict_arguments = {}

        # Get if yes or not the container have a arguments to set
        self.__logger.log(
            "Est-ce que cette image Docker possède des arguments / variables d'environnements a saisir ?")
        has_arguments = self.__cli_utils.yes_no()

        # Yes
        if has_arguments == 0:
            self.__logger.log("> Oui", "dark_grey")
            currently_add_arguments = 0
            while(True):
                # Add (new) arguments
                if currently_add_arguments == 0:
                    name_arguments = input("Nom de l'argument : ")
                    value_arguments = input("Valeur de l'argument : ")
                    dict_arguments[name_arguments] = value_arguments

                    # Ask if the user wants to add another argument
                    self.__logger.log(
                        "Voulez-vous ajoutez un nouvelle argument ?")
                    currently_add_arguments = self.__cli_utils.yes_no()
                    if currently_add_arguments == 0:
                        self.__logger.log("> Oui", "dark_grey")

                # Stop adding arguments
                else:
                    self.__logger.log("> Non", "dark_grey")
                    self.docker_container_template.arguments = dict_arguments
                    return

        # No
        else:
            self.__logger.log("> Non", "dark_grey")

            # if dict is empty
            if bool(dict_arguments) == False:
                self.docker_container_template.arguments = {}
            return

    def get_ports(self):
        '''Ask the user to give the required ports to expose to run the container'''

        while(True):
            # Get if yes or not the container have a port to set
            self.__logger.log(
                "Est-ce que cette image Docker possède un port à mapper ?", "white")
            has_port = self.__cli_utils.yes_no()

            # Yes
            if has_port == 0:
                self.__logger.log("> Oui", "dark_grey")
                dict_port = {}

                while True:
                    port_entrant = input("Port du container : ")
                    if port_entrant.isnumeric():
                        break

                while True:
                    port_sortant = input("Port de la machine host : ")
                    if port_sortant.isnumeric():
                        break

                dict_port[port_entrant + "/tcp"] = port_sortant
                self.docker_container_template.ports = dict_port
                return

            # No
            else:
                self.__logger.log("> Non", "dark_grey")
                self.docker_container_template.ports = {}
                return

    def get_name_container(self):
        '''Ask the user to give a name to the container if required.'''

        container_name = input(
            "Nom du container (si vide, un nom par defaut sera donnés) : ")
        if container_name is None or container_name == "":
            container_name = self.docker_container_template.image_name + "_container"

        container_name = container_name.replace(":", "_").replace("/", "_")
        self.__logger.log(f"{container_name}", "dark_grey")
        self.docker_container_template.container_name = container_name

    def add_another_image(self) -> bool:
        '''
        Ask the user if he wants to add another image to the cluster.

        Returns True if the user want, False otherwise
        '''

        self.docker_cluster_template.list_docker_containers_templates.append(
            self.docker_container_template)
        self.__logger.log(
            "Voulez-vous choisir une autre image Docker en plus à lancer ?")
        another_image = self.__cli_utils.yes_no()

        # Yes
        if another_image == 0:
            self.__logger.log("> Oui", "dark_grey")
            # Reset the docker container template for the next image
            self.docker_container_template = DockerContainerTemplate()
            return True

        # No
        else:
            self.__logger.log("> Non", "dark_grey")
            return False

    def get_token(self):
        '''Ask the user to enter a token'''
        token = input("Veuillez saisir votre token de connexion : ")
        return token

    def display_logo_ASCII(self):
        '''Display the logo in ASCII format'''
        __WATTSTACK = """
         __        __    _   _   ____  _             _    
         \ \      / /_ _| |_| |_/ ___|| |_ __ _  ___| | __
          \ \ /\ / / _` | __| __\___ \| __/ _` |/ __| |/ /
           \ V  V / (_| | |_| |_ ___) | || (_| | (__|   < 
            \_/\_/ \__,_|\__|\__|____/ \__\__,_|\___|_|\_\

        """
        self.__logger.log(__WATTSTACK)

    def get_docker_cluster_info(self):
        '''Get information about the cluster itself, or general information such the time we collect data or the report name'''

        self.get_name_for_report()

        # Get the duration while we collect data for the report
        while(True):

            # ask user the time we collect data
            is_time_valid = self.get_duration_collect_data()

            # if the given time is a number
            if is_time_valid is True:
                break
            else:
                pass

    def get_docker_container_info(self) -> bool:
        '''Get the information about the docker container, such as the image, arguments and ports'''
        self.get_image_name()
        self.get_name_container()
        self.get_arguments()
        self.get_ports()

    def get_docker_informations(self):
        '''Get all the informations required to successfully run the docker cluster / containers and send the data afterwards'''
        self.get_docker_cluster_info()
        self.get_docker_container_info()

        # Ask if the user want to add another container
        while(True):
            add_another_container = self.add_another_image()
            if add_another_container is True:
                self.get_docker_container_info()
            else:
                break

    def login(self, http_helper: HTTPHelper):
        '''Ask the user for a token, and try it.'''

        # Check if user run the program giving a token
        token = self.__arguments_utils.get_argument_token()

        while(True):
            # ask token
            if token is None:
                token = self.get_token()

            # check if it valid
            is_valid = http_helper.try_token(token)

            # if not, retry
            if is_valid == True:
                break

            # else, ask if user when to retry
            else:
                self.__cli_utils.retry()
                token = None
                self.__logger.log("> Réesayer", "dark_grey")

    def choose_default_docker_cluster(self):
        '''Propose a list of default docker clusters to the user, he can choose one of them of create it own cluster

        Returns True if he choose a default one, False otherwise.

        Also return the index if false, required to get the default cluster the user wants to use'''

        self.__logger.log(
            "Voulez-vous lancer un cluster pré-fait, ou choisir vous-même ?")

        list_name_cluster = self.list_default_docker_cluster.get_name_default_container()
        # "None" create a space in the CLI, but have no index, we will need to add a +1 to index to know if user choose the last one
        list_name_cluster.append(None)
        list_name_cluster.append("Je créer mon cluster Docker")

        index = self.__cli_utils.terminal_menu(list_name_cluster)
        self.__logger.log(f"> {list_name_cluster[index]}", "dark_grey")

        # +1 because "None" have no index, the last available index is equals to the list-1
        if index+1 == len(list_name_cluster):
            return False, index
        else:
            return True, index

    def get_stack_informations(self):
        '''Ask the user if he wants to choose a default stack or not.

        If yes, select the stack, and ask the general information

        Otherwise, ask the user about the general information and the docker information'''

        # ask if the user want to run a default stack, or a personal stack
        choose_default_cluster, cluster_index = self.choose_default_docker_cluster()

        # default stack
        if choose_default_cluster is True:
            self.docker_cluster_template = self.list_default_docker_cluster.get_specific_default_container(
                cluster_index)
            self.get_docker_cluster_info()
        else:
            # get docker related data
            self.get_docker_informations()

    def get_data_from_user(self, http_helper: HTTPHelper):
        '''Log-in the user, and then ask the information related to the stack he choose'''
        # initialize the http helper
        self.init_HTTPHelper(http_helper)

        # display LOGO
        self.display_logo_ASCII()

        # login user
        self.login(http_helper)

        # get information related to the stack / cluster
        self.get_stack_informations()

    def get_data_from_user_passwordless(self, http_helper: HTTPHelper):
        '''Ask the user the information related to the stack he choose'''
        # initialize the http helper
        self.init_HTTPHelper(http_helper)

        # display LOGO
        self.display_logo_ASCII()

        # get information related to the stack / cluster
        self.get_stack_informations()

    def send_data_to_server(self, report: Report):
        '''Send data to the server, if it doesn't work, ask the user if he want to retry'''
        self.http_helper = HTTPHelper()
        while(True):
            is_send = self.http_helper.post_report(report)

            if is_send is True:
                return
            else:
                self.__cli_utils.retry()
