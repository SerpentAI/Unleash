import uuid
import pathlib

import numpy as np

import skimage.io
import skimage.color

from PIL import Image as PILImage


class Image:
    def __init__(self, array=None):
        if not isinstance(array, np.ndarray):
            raise ValueError("'array' should be a NumPy array...")

        self.uuid = str(uuid.uuid4())
        self.array = self._as_uint8_rgba(array)

    @property
    def width(self):
        return self.array.shape[1]

    @property
    def height(self):
        return self.array.shape[0]

    @property
    def short_side(self):
        return min(self.width, self.height)

    @property
    def long_side(self):
        return max(self.width, self.height)

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def area(self):
        return self.width * self.height

    @property
    def area_non_zero(self):
        return np.sum(self.array[:, :, 0] > 0)

    @property
    def has_transparency(self):
        return np.min(self.array[:, :, 3]) < 255

    @property
    def rgba(self):
        return self.array

    @property
    def rgba_normalized(self):
        return np.array(self.array, dtype=np.float64) / 255.0

    @property
    def alpha(self):
        return self.array[:, :, 3]

    @property
    def rgb(self):
        return self.array[:, :, :3]

    @property
    def rgb_normalized(self):
        return np.array(self.array[:, :, :3], dtype=np.float64) / 255.0

    @property
    def lab(self):
        return skimage.color.rgb2lab(self.rgb)

    @property
    def lab_normalized(self):
        lab_array = self.lab

        lab_array[:, :, 0] = lab_array[:, :, 0] / 100.0
        lab_array[:, :, 1] = (lab_array[:, :, 1] + 128.0) / 255.0
        lab_array[:, :, 2] = (lab_array[:, :, 2] + 128.0) / 255.0

        return lab_array

    @property
    def as_pil(self):
        return PILImage.fromarray(self.array)

    def save(self, file_path=None):
        # TODO: Robust implementation with format options?
        self.as_pil.save(file_path)

    @classmethod
    def from_file(cls, file_path):
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)

        if not file_path.is_file():
            raise FileNotFoundError()

        try:
            array = skimage.io.imread(file_path)
        except ValueError:
            raise ValueError(f"Invalid image data: 'f{file_path}'")

        return cls(array)

    @classmethod
    def copy(cls, image=None, keep_uuid=False):
        if not isinstance(image, cls):
            raise TypeError("'image' should be of type Image...")

        image_copy = cls(image.array)

        if keep_uuid:
            image_copy.uuid = image.uuid

        return image_copy

    @staticmethod
    def _as_uint8_rgba(array):
        # Handle boolean and normalized float arrays
        if array.dtype == np.bool:
            array = np.array(array, dtype=np.uint8) * 255
        elif array.dtype == np.float64:
            if np.max(array) <= 1.0:
                array = array * 255.0

            array = np.array(array, dtype=np.uint8)

        if array.dtype != np.uint8:
            raise TypeError(f"Unsupported image array dtype: '{array.dtype}'")

        # Force Grayscale to RGB
        if len(array.shape) == 2:
            array = skimage.color.gray2rgb(array)

        # Force RGB to RGBA
        if array.shape[2] == 3:
            array = np.array(PILImage.fromarray(array).convert("RGBA"))

        return array
