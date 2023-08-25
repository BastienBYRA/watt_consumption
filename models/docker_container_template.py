class DockerContainerTemplate:
    def __init__(self, image_name: str = None, arguments: dict = None, ports: dict = None, container_name: str = None):
        self.container_name = container_name
        self.image_name: str = image_name
        self.arguments: dict[str, str] = arguments
        self.ports: dict[str, str] = ports
        
    def set_image_name(self, image_name):
        self.image_name = image_name
        
    def set_arguments(self, arguments):
        self.arguments = arguments
    
    def set_ports(self, ports):
        self.ports = ports
        
    def set_container_name(self, container_name):
        self.container_name = container_name