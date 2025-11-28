from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class ComputeDiscovery(DiscoveryBase):
    def list_servers(self) -> Iterable[Any]:
        self.logger.info("Discovering servers...")
        # Use details=True to get addresses and other metadata
        return self._safe_list(self.conn.compute.servers, details=True, project_id=self.project_id)

    def list_flavors(self) -> Iterable[Any]:
        self.logger.info("Discovering flavors...")
        return self._safe_list(self.conn.compute.flavors)

    def list_keypairs(self) -> Iterable[Any]:
        self.logger.info("Discovering keypairs...")
        return self._safe_list(self.conn.compute.keypairs)
    
    def list_server_groups(self) -> Iterable[Any]:
        self.logger.info("Discovering server groups...")
        return self._safe_list(self.conn.compute.server_groups)

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        return {
            "servers": self.list_servers(),
            "flavors": self.list_flavors(),
            "keypairs": self.list_keypairs(),
            "server_groups": self.list_server_groups()
        }
