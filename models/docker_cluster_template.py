from models.docker_container_template import DockerContainerTemplate


class DockerClusterTemplate:
    def __init__(self, presentation_name: str = "", docker_container_template: DockerContainerTemplate = []):
        self.presentation_name: str = presentation_name
        self.list_docker_containers_templates: list[DockerContainerTemplate] = docker_container_template
        
    def get_name_all_containers(self) -> list[str]:
        '''Returns a list of all containers images names'''
        list_names = []
        for container in self.list_docker_containers_templates:
            list_names.append(container.image_name)
        return list_names