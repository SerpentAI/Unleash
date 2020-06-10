import pathlib

from unleash.nodes.input_node import InputNode
from unleash.image import Image

from unleash.logger import logger


class FileInputNode(InputNode):
    def __init__(self, name=None, path=None):
        super().__init__(name=name)

        self.type = "FileInputNode"

        self.path = path

        self.validate()

    def run(self, socket_paths=None, output_path=None):
        try:
            image = Image.from_file(self.path)

            self.create_output_path(output_path)

            image_path = output_path.joinpath(f"{image.uuid}.png")

            logger.info(f"[FileInputNode] Saving '{image.uuid}.png' output path...")
            image.save(image_path)
        except Exception as e:
            self.has_failed = True
            self.exceptions.append(e)

            return False

        self.is_complete = True

        return {"main": output_path}

    def validate(self):
        if self.path is None or not isinstance(self.path, (str, pathlib.Path)):
            self.validation_messages.append(
                "[FileInputNode] 'path' should be one of: 'str', 'pathlib.Path'"
            )

            self.is_valid = False
            return False

        if isinstance(self.path, str):
            self.path = pathlib.Path(self.path)

        if not self.path.is_file():
            self.validation_messages.append(
                f"[FileInputNode] '{self.path.absolute().as_posix()}' is not a file"
            )

            self.is_valid = False
            return False

        try:
            Image.from_file(self.path)
        except ValueError:
            self.validation_messages.append(
                f"[FileInputNode] '{self.path.absolute().as_posix()}' is not a valid image"
            )

            self.is_valid = False
            return False

        self.is_valid = True
        return True

    @staticmethod
    def node_description():
        return "FileInputNode is an input node that inserts a single image into the pipeline"

    @staticmethod
    def node_kwargs():
        return [
            {
                "name": "path",
                "label": "Image Path",
                "description": "A file path to an image",
                "type": "FILE_PATH",
                "default_value": None,
                "allow_empty": False,
            },
        ]
