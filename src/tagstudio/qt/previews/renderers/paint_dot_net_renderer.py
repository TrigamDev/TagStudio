import base64
import struct
import xml.etree.ElementTree as ElementTree
from io import BytesIO

import structlog
from PIL import Image

from tagstudio.qt.previews.renderers.base_renderer import BaseRenderer, RendererContext

logger = structlog.get_logger(__name__)

thumbnail_path_within_zip: str = "preview.png"


class PaintDotNetRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def render(context: RendererContext) -> Image.Image | None:
        """Extract and render a thumbnail for a Paint.net file.

        Args:
            context (RendererContext): The renderer context.
        """
        with open(context.path, "rb") as paint_net_file:
            try:
                # First 4 bytes are the magic number
                if paint_net_file.read(4) != b"PDN3":
                    return None

                # Header length is a little-endian 24-bit int
                header_size = struct.unpack("<i", paint_net_file.read(3) + b"\x00")[0]
                thumb_element = ElementTree.fromstring(paint_net_file.read(header_size)).find(
                    "./*thumb"
                )
                if thumb_element is None:
                    return None

                encoded_png = thumb_element.get("png")
                if encoded_png:
                    decoded_png = Image.open(BytesIO(base64.b64decode(encoded_png)))
                    if decoded_png.mode == "RGBA":
                        rendered_image = Image.new("RGB", decoded_png.size, color="#1e1e1e")
                        rendered_image.paste(decoded_png, mask=decoded_png.getchannel(3))
                        return rendered_image
            except Exception as e:
                logger.error(
                    "[PaintDotNetRenderer]Couldn't render thumbnail", path=context.path, error=e
                )

        return None
