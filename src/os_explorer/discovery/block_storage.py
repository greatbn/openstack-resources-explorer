from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class BlockStorageDiscovery(DiscoveryBase):
    def list_volumes(self) -> Iterable[Any]:
        self.logger.info("Discovering volumes...")
        return self._safe_list(self.conn.block_storage.volumes, project_id=self.project_id)

    def list_snapshots(self) -> Iterable[Any]:
        self.logger.info("Discovering snapshots...")
        return self._safe_list(self.conn.block_storage.snapshots, project_id=self.project_id)

    def list_backups(self) -> Iterable[Any]:
        self.logger.info("Discovering backups...")
        return self._safe_list(self.conn.block_storage.backups, project_id=self.project_id)

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        return {
            "volumes": self.list_volumes(),
            "snapshots": self.list_snapshots(),
            "backups": self.list_backups()
        }
