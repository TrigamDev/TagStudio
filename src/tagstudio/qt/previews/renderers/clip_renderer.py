import base64
import sqlite3
import struct
import xml.etree.ElementTree as ElementTree
from io import BytesIO

import structlog
from PIL import Image

from tagstudio.qt.previews.renderers.base_renderer import BaseRenderer, RendererContext

logger = structlog.get_logger(__name__)

thumbnail_path_within_zip: str = "preview.png"


class ClipStudioPaintRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def render(context: RendererContext) -> Image.Image | None:
        """Extract and render a thumbnail for a Clip Studio Paint file.

        Args:
            context (RendererContext): The renderer context.
        """
        try:
            with open(context.path, "rb") as clip_file:
                blob = clip_file.read()
                sqlite_index = blob.find(b"SQLite format 3")
                if sqlite_index == -1:
                    return None

            with sqlite3.connect(":memory:") as conn:
                conn.deserialize(blob[sqlite_index:])
                thumbnail = conn.execute("SELECT ImageData FROM CanvasPreview").fetchone()
                if thumbnail:
                    return Image.open(BytesIO(thumbnail[0]))
        except Exception as e:
            logger.error("Couldn't render thumbnail", path=context.path, error=e)

        return None
