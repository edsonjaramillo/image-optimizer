from os import path, listdir
from typing import Tuple
from PIL import Image


class Optimizer:
    def optimize_images(self, image_paths: list, destination_path: str, min_dimension: int) -> str:
        """Optimize images.

        Arguments:
            `image_paths` (list): The paths of the images to optimize.
            `destination_path` (str): The path of the directory to save the optimized images.
            `min_dimension` (int): The minimum dimension of the image to reduce to.

        Returns: `str`
            `percentage_saved` (str): The percentage of the optimized images."""

        files_did_not_get_optimized: list[str] = []
        bytes_unoptimized = 0

        for image_path in image_paths:
            bytes_unoptimized += path.getsize(image_path)
            filename = self.__remove_paths(image_path)
            new_filename = f"{destination_path}/{self.__file_format(filename, '.webp')}"
            image = Image.open(image_path)
            WIDTH, HEIGHT = image.size

            if self.__is_optimized(WIDTH, HEIGHT, min_dimension):
                files_did_not_get_optimized.append(filename)
                image.save(fp=new_filename, quality=80)
                continue

            W, H = self.__get_new_dimensions(WIDTH, HEIGHT, min_dimension)

            resized_image = image.resize((W, H))
            resized_image.save(fp=new_filename, quality=80)

        bytes = self.__get_optimized_bytes(destination_path)
        percentage_saved = self.__percentage_optimized(bytes_unoptimized, bytes)
        return percentage_saved

    def __is_optimized(self, width: int, height: int, min_dimension: int) -> bool:
        """Check if the image is optimized.

        Arguments:
            `width` (int): The width of the image.
            `height` (int): The height of the image.
            `min_dimension` (int): The minimum dimension of the image to reduce to.

        Returns: `bool`
            `True` if the image is optimized. `False` if the image is not optimized."""

        if width < min_dimension or height < min_dimension:
            return True

        return False

    def __remove_paths(self, image_path: str) -> str:
        """Remove the paths of the images.
        Ex: `/ home/user/images/image.jpg` -> `image.jpg`

        Arguments:
            `image_path` (str): The path of the image to remove the path from.
        Returns: `str`
            `filename` (str): The filename of the image."""
        return image_path.split('/')[-1]

    def __get_new_dimensions(self, width: int, height: int, min_dimension: int) -> Tuple[int, int]:
        """Calculate the new dimensions of the image.

        Arguments:
            `width` (int): The width of the image.
            `height` (int): The height of the image.
            `min_dimension` (int): The minimum dimension of the image to reduce to.

        Returns: `tuple -> (int, int)`
            `new_width` (int): The new width of the image.
            `new_height` (int): The new height of the image."""
        if width < min_dimension or height < min_dimension:
            return (width, height)

        width_decrement = width / 1000
        height_decrement = height / 1000

        while True:
            width = width - width_decrement
            height = height - height_decrement
            if width < min_dimension or height < min_dimension:
                return (int(width), int(height))

    def __file_format(self, filename: str, extension: str) -> str:
        """Return the file with a diffferent extension.
        Ex: `image.jpg` -> `image.webp`

        Arguments:
            `filename` (str): The filename of the image
            `extension` (str): The extension of the image.
        Returns: `str`
            `filename` (str): The filename of the image with the webp extension."""
        return filename.split('.')[0] + extension

    def __get_optimized_bytes(self, destination_path: str) -> int:
        """Get the bytes of the optimized images.

        Arguments:
            `destination_path` (str): The path of the directory to get the bytes from.

        Returns: `int`
            `bytes` (int): The bytes of the optimized images."""
        bytes = 0
        files = listdir(destination_path)
        for file in files:
            bytes += path.getsize(f"{destination_path}/{file}")

        return bytes

    def __percentage_optimized(self, unoptimized: int, optimized: int) -> str:
        """Get the percentage of the optimized images.

        Arguments:
            `unoptimized` (int): The bytes of the unoptimized images.
            `optimized` (int): The bytes of the optimized images.

        Returns: `str`
            `percentage` (str): The percentage of the optimized images."""

        change = ((optimized - unoptimized) / unoptimized) * 100
        rounded = abs(round(change, 2))
        return f"{rounded}%"


def main() -> None:
    paths = ['C:/Users/edson/Downloads/pexels-thái-huỳnh-3998365.jpg',
             'C:/Users/edson/Downloads/pexels-no-name-66997.jpg']
    destination = 'C:/Users/edson/Desktop/cms/finished'
    min_dimension = 700

    Optimizer().optimize_images(paths, destination, min_dimension)
