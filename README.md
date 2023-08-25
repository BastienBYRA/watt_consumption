# **WattStack CLI / Watt Consumption**

Ce projet permet de lancer des containers (prédéfinis ou personnalisés) et récupérer des données (consommation watt, CPU / RAM usage).

Le projet est uniquement fonctionnel sur Linux, car un composant nécessaire à l'application (libglib2.0-dev) est uniquement disponible sur Linux.

Note : Cette CLI est un projet étudiant, et n'est à l'heure d'aujourd'hui pas destinée à être utilisée en production.

## **Requirements**

- Docker (https://www.docker.com/)
- libglib2.0-dev
  - Linux : `sudo apt-get install libglib2.0-dev`

## **Lancer le projet**

Cloner le projet : `git clone https://github.com/thclmnt/projet-iut.git`
/!\ Dans models/Probe.py, dans la fonction `connect_socket()`, changer la variable `IP_SOCKET` par l'IP de votre Wattmètre

- <u>Depuis le code</u> :
  - PREREQUIS :
    - Python : (https://www.python.org/downloads/)
    - Pip _(Vous devriez probablement l'avoir après avoir installer Python)_ : (https://packaging.python.org/en/latest/tutorials/installing-packages/)
  - Aller dans le dossier de l'application : `watt_consumption`
  - `pip install -r requirements.txt`
  - Lancer le projet avec la commande : `python3 main.py` OU `py main.py` OU `python main.py`

<br>

- <u>Avec Docker</u> :
  - Créer l'image Docker : `docker build -t watt_consumption .`
  - Lancer le projet : `docker run -v PATH_TO_YOUR_DOCKER_DAEMON:/var/run/docker.sock -it watt_consumption`
    - Exemple : `docker run -v /var/run/docker.sock:/var/run/docker.sock -it watt_consumption`
