import zipfile
import logging
import io
import json
from typing import BinaryIO
from .utils import Timer
from . import models


class VPRParser:
    def __init__(self) -> None:
        self.logger = logger = logging.getLogger(__name__)

    def _read_as_dict(
        self, fp: BinaryIO, timer: Timer, filename: str = "project.vpr"
    ) -> dict:
        zf = zipfile.ZipFile(fp, "r")  # wrap it again to avoid ext check
        timer.add_part("unzip_file")
        content = zf.open("Project/sequence.json", "r")
        timer.add_part("open_file")
        data = json.load(content)
        timer.add_part("parse_json")
        content.close()
        zf.close()
        timer.add_part("cleanup_fp")
        return data

    def _parse_from_bytesio(
        self, fp: io.BytesIO, filename: str = "project.vpr"
    ) -> models.VPRFile:
        self.logger.debug('Loading VPR file "%s" as VPRFile object', filename)
        timer = Timer("parse_vpr")
        json_data = self._read_as_dict(fp, timer, filename)
        model = models.VPRFile(**json_data)
        timer.end("load_as_pydantic_model")
        self.logger.debug(timer.as_human_readable())
        return model

    def parse(self, filename: str) -> models.VPRFile:
        with open(filename, "rb") as fp:
            return self._parse_from_bytesio(
                io.BytesIO(fp.read()), filename.split("/")[-1]
            )

    def _dump_to_bytesio(
        self, model: models.VPRFile, bytesio: io.BytesIO
    ) -> None:
        self.logger.debug("Dumping VPRFile object to BytesIO")
        timer = Timer("dump_vpr")
        json_data = model.dict(by_alias=True, exclude_none=True)
        timer.add_part("dictify_model")
        json_str = json.dumps(json_data, separators=(",", ":"))  # saves space!
        timer.add_part("stringify_json")
        zf = zipfile.ZipFile(bytesio, "w")
        zf.writestr("Project/sequence.json", json_str)
        zf.close()
        timer.end("create_zip_file")
        self.logger.debug(timer.as_human_readable())

    def dump(self, model: models.VPRFile, filename: str) -> None:
        with open(filename, "wb") as fp:
            fake_io = io.BytesIO()
            self._dump_to_bytesio(model, fake_io)
            fp.write(fake_io.getvalue())
