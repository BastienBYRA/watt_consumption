from time import sleep
import threading
from services.data_collect_services import DataCollectService
from utils.logger import Logger
from models.report import Report
from models.Probe import Probe
from cli import CLI
from services.docker_services import DockerService
from helpers.http_helpers import HTTPHelper
from threading import Event
from helpers.thread_helpers import ThreadHelper
from datetime import datetime, timedelta


class MainApp:
    def __init__(self):
        self.__cli: CLI | None = CLI()
        self.__docker_helper: DockerService | None = DockerService()
        self.__http_helper: HTTPHelper | None = HTTPHelper()
        self.__data_collect_helper: DataCollectService | None = DataCollectService()

    def run(self):

        # # Authentification and Get the list of images, arguments and ports from the user
        # self.__cli.get_data_from_user(self.__http_helper)

        # Ask the user to choose what stack he wants to run, no login to avoid the need of a server
        self.__cli.get_data_from_user_passwordless(self.__http_helper)

        # Initialize the network
        self.__docker_helper.create_default_network()

        # Run all docker images and check they are running
        self.__docker_helper.run_all_docker_image(
            self.__cli.docker_cluster_template)

        # Collecte les données
        self.__data_collect_helper.collect(
            self.__docker_helper, threading.Event(), self.__cli.duration_collect_data)

        # Create a Report object
        report: Report = Report(report_name=self.__cli.report_name, date_start=self.__data_collect_helper.date_start, date_end=self.__data_collect_helper.date_end,
                                token=self.__http_helper.token, list_images=self.__cli.docker_cluster_template.get_name_all_containers(),
                                list_mesures_power=self.__data_collect_helper.list_watts_stats, list_mesures_pc=self.__data_collect_helper.list_cpu_and_ram_stats)

        # # POST the Report object to the server
        # self.__cli.send_data_to_server(report)

        # Print the report, no POST to avoid the need of a server
        report_json = report.destructuring()
        print(report_json)

        # Remove all existing containers
        self.__docker_helper.kill_all_container()


# Create an instance of the MainApp class and run the application
app = MainApp()
app.run()
