import uuid

from unleash.logger import logger


class Node:
    def __init__(self, name=None):
        self.uuid = str(uuid.uuid4())
        self.name = name or self.uuid

        self.input_sockets = {"main"}
        self.output_sockets = {"main"}

        self.is_valid = False
        self.is_complete = False

        self.has_failed = False

        self.validation_messages = list()
        self.exceptions = list()

    def register_input_socket(self, name):
        self.input_sockets.add(name)
        return True

    def register_output_socket(self, name):
        self.output_sockets.add(name)
        return True

    def unregister_input_socket(self, name, force=False):
        if name == "main" and force is False:
            logger.warning("Main sockets should not be removed. Ignoring!")
            return False

        if name in self.input_sockets:
            self.input_sockets.remove(name)
            return True

        return False

    def unregister_output_socket(self, name, force=False):
        if name == "main" and force is False:
            logger.warning("Main sockets should not be removed. Ignoring!")
            return False

        if name in self.input_sockets:
            self.output_sockets.remove(name)
            return True

        return False

    def create_output_path(self, output_path):
        logger.debug(f"Creating node output path: {output_path.absolute().as_posix()}")
        output_path.mkdir(parents=True, exist_ok=True)

        return True

    def validate(self):
        raise NotImplementedError()

    def check_prerequisites(self):
        return True

    def handle_prerequisites(self):
        return True


class NodeFile:
    extension = ".unn"

    def __init__(self):
        pass
