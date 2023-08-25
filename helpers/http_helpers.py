from datetime import datetime
from enum import Enum
import json
import requests
from sys import exit

from models.report import Report
from utils.logger import Logger
from simple_term_menu import TerminalMenu


class URLOperation(Enum):
    POST_TOKEN = "cli/token/authorize"
    POST_REPORT = 'report'
    GET_REPORT = 'report/'


class HTTPHelper:
    def __init__(self):
        self.__api_url: str | None = 'YOUR API URL'
        self.__front_url: str | None = 'YOUR FROND-END URL'
        self.token: str | None = None
        self.__logger: Logger = Logger("HTTP_HELPER")

    def try_token(self, token: str) -> bool:
        '''Try the given token

        Args:
            token (str): The token given by the user to log in

        Returns:
            True if the token is valid, False otherwise'''

        try:
            response = requests.post(self.__api_url + URLOperation.POST_TOKEN.value,
                                     data={"token": token})

        except requests.ConnectionError:
            self.__logger.log(
                "Impossible d'atteindre le serveur, arret du programme.", "red")
            exit(1)

        # Success
        if response.status_code == 200:
            self.token = token
            self.__logger.log("Vous êtes authentifier ! \r\n", "green")
            return True

        # Failure
        else:
            self.__logger.log(
                "Échec de l'authentification, veillez à ce que le token soit valide et non utilisé.", "red")
            return False

    def post_report(self, report: Report) -> bool:
        '''Send the report to the server

        Returns:
            True if the report was sent successfully, False otherwise'''

        try:
            response = requests.post(self.__api_url + URLOperation.POST_REPORT.value, headers={
                                     'Content-Type': 'application/json'}, data=report.destructuring())
        except requests.ConnectionError:
            self.__logger.log(
                "Impossible d'atteindre le serveur, arret du programme.", "red")
            return False

        # Success
        if(response.status_code == 201):
            self.__logger.log("Envoi des données réussi !", "green")
            self.__logger.log(
                f"Consulter le rapport à cette URL : {self.__front_url + URLOperation.GET_REPORT.value + report.token}")
            return True

        # Failure
        else:
            self.__logger.log("Échec de l'envoi des données.", "red")
            return False
