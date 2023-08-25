from models.docker_cluster_template import DockerClusterTemplate
from models.docker_container_template import DockerContainerTemplate


class DefaultDockerCluster:
    def __init__(self):
        '''DefaultDockerCluster is a class that contains multiple instances of DockerClusterTemplate to allow user to try to run some stack without actually having to write it himself'''
        
        self.alpine_node_instance_config: DockerClusterTemplate = DockerClusterTemplate("Alpine Linux + Node",
            [
                DockerContainerTemplate("alpine:latest",{},{}, "alpine_container"),
                DockerContainerTemplate("node:latest",{},{}, "node_container"),
            ]
        )
        
        self.symfony_maria_instance_config: DockerClusterTemplate = DockerClusterTemplate("Application Symfony + MariaDB",
            [
                DockerContainerTemplate(
                    "bitnami/symfony:latest",
                    {
                        'SYMFONY_PROJECT_NAME': 'myapp',
                        'MARIADB_HOST': 'mariadb',
                        'MARIADB_PORT_NUMBER': '3306',
                        'MARIADB_USER': 'bobby',
                        'MARIADB_PASSWORD': 'tables',
                        'MARIADB_DATABASE': 'myapp',
                        'ALLOW_EMPTY_PASSWORD' : 'yes',
                        'SYMFONY_PROJECT_SKELETON' : 'symfony/skeleton',
                    },
                    {'8000/tcp': 0},
                    "symfony_bitnami_container"
                ),
                DockerContainerTemplate(
                    'bitnami/mariadb:10.11',
                    {
                        'ALLOW_EMPTY_PASSWORD': 'yes',
                        'MARIADB_USER': 'bobby',
                        'MARIADB_PASSWORD': 'tables',
                        'MARIADB_DATABASE': 'myapp'
                    },
                    {},
                    "mariadb_bitnami_container"
                ),
            ]
        )
        
        self.express_mongo_instance_config: DockerClusterTemplate = DockerClusterTemplate("Interface administrateur MongoDB avec Express",
            [
                DockerContainerTemplate("mongo",
                    {
                        "MONGO_INITDB_ROOT_USERNAME": "rootuser",
                        "MONGO_INITDB_ROOT_PASSWORD": "rootpass",
                    },
                    {},
                    "mongodb_container"
                ),
                DockerContainerTemplate("mongo-express",
                    {
                        'ME_CONFIG_MONGODB_ADMINUSERNAME': 'rootuser',
                        'ME_CONFIG_MONGODB_ADMINPASSWORD': 'rootpass',
                        'ME_CONFIG_MONGODB_SERVER': 'mongodb_container'
                    },
                    {'8081/tcp': '8081'},
                    "mongo-express_container"
                ),
            ]
        )

        
    
    def get_name_default_container(self) -> list[str]:
        return [self.alpine_node_instance_config.presentation_name, self.symfony_maria_instance_config.presentation_name,
                self.express_mongo_instance_config.presentation_name]
        
    def get_specific_default_container(self, index) -> DockerClusterTemplate:
        list_default_container = [self.alpine_node_instance_config, self.symfony_maria_instance_config,
                                  self.express_mongo_instance_config]
        
        return list_default_container[index]
        
        