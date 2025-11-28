from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class ImageDiscovery(DiscoveryBase):
    def list_images(self) -> Iterable[Any]:
        self.logger.info("Discovering images...")
        return self._safe_list(self.conn.image.images)

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        return {
            "images": self.list_images()
        }
