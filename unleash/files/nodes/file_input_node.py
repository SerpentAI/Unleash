import uuid
import pathlib

from unleash.nodes.input_node import InputNode


class FileInputNode(InputNode):
    def __init__(self, path=None):
        super().__init__()

        self.uuid = str(uuid.uuid4())
        self.path = path

        self.is_valid = self._validate()
        self.is_complete = False

        self.has_failed = False

    def run(self, output_path=None):
        pass

    def _validate(self):
        pass

    @staticmethod
    def node_kwargs():
        pass
