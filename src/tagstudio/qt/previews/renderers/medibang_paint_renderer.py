import os
import struct
import xml.etree.ElementTree as ElementTree
import zlib

import structlog
from PIL import Image

from tagstudio.core.utils.types import unwrap
from tagstudio.qt.previews.renderers.base_renderer import BaseRenderer, RendererContext

logger = structlog.get_logger(__name__)

thumbnail_path_within_zip: str = "preview.png"


class MedibangPaintRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def render(context: RendererContext) -> Image.Image | None:
        """Extract and render a thumbnail for a Medibang Paint or FireAlpaca file.

        Args:
            context (RendererContext): The renderer context.
        """
        try:
            with open(context.path, "rb") as f:
                magic = struct.unpack("<7sx", f.read(8))[0]
                if magic != b"mdipack":
                    return None

                bin_header = struct.unpack("<LLL", f.read(12))
                xml_header = ElementTree.fromstring(f.read(bin_header[1]))

                mdibin_count = len(xml_header.findall("./*Layer")) + 1
                for _ in range(mdibin_count):
                    pac_header = struct.unpack("<3sxLLLL48s64s", f.read(132))
                    if not pac_header[6].startswith(b"thumb"):
                        f.seek(pac_header[3], os.SEEK_CUR)
                        continue

                    thumb_element = unwrap(xml_header.find("Thumb"))
                    dimensions = (
                        int(unwrap(thumb_element.get("width"))),
                        int(unwrap(thumb_element.get("height"))),
                    )

                    thumb_blob = f.read(pac_header[3])
                    if pac_header[2] == 1:
                        thumb_blob = zlib.decompress(thumb_blob, bufsize=pac_header[4])

                    return Image.frombytes("RGBA", dimensions, thumb_blob, "raw", "BGRA")
                    break
        except Exception as e:
            logger.error(
                "[MedibangPaintRenderer] Couldn't render thumbnail", path=context.path, error=e
            )

        return None
