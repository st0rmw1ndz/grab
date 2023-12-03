from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor


# TODO: add tqdm progress bar
class Uploader(ABC):
    """Represents a generic uploader."""

    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    @abstractmethod
    def upload(self, file: Path) -> str:
        """Uploads a file to the uploader.

        :param file: File to upload
        :return: URL of the uploaded file
        """
        pass

    def post(self, params: dict[str, Any]) -> requests.Response:
        """Performs a POST request to the uploader.

        :param params: Request parameters
        :return: Response object
        """
        encoder = MultipartEncoder(fields=params)
        monitor = MultipartEncoderMonitor(encoder=encoder)
        resp = requests.post(
            self.api_url,
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )
        return resp
