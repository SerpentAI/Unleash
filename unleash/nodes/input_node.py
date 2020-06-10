from unleash.node import Node

from unleash.logger import logger


class InputNode(Node):
    def __init__(self, name=None):
        super().__init__(name=name)

        self.unregister_input_socket("main", force=True)

    def register_input_socket(self, name):
        logger.warning("Input nodes cannot have input sockets!")
        return False
