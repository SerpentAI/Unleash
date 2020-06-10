from unleash.node import Node

from unleash.logger import logger


class OutputNode(Node):
    def __init__(self, name=None):
        super().__init__(name=name)

        self.unregister_output_socket("main", force=True)

    def register_output_socket(self, name):
        logger.warning("Output nodes cannot have output sockets!")
        return False
