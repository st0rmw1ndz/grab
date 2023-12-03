import mimetypes
from pathlib import Path

from grab.uploader import Uploader


class CatboxUploader(Uploader):
    def __init__(self) -> None:
        self.api_url = "https://catbox.moe/user/api.php"

    def upload(self, file: Path) -> str:
        params = {
            "reqtype": "fileupload",
            "userhash": "",
            "fileToUpload": (
                file.name,
                file.read_bytes(),
                mimetypes.guess_type(file.name)[0],
            ),
        }
        resp = self.post(params)
        return resp.text
