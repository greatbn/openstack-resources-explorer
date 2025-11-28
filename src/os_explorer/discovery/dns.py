from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class DNSDiscovery(DiscoveryBase):
    def list_zones(self) -> Iterable[Any]:
        self.logger.info("Discovering zones...")
        return self._safe_list(self.conn.dns.zones, project_id=self.project_id)

    def list_recordsets(self, zone_id: str) -> Iterable[Any]:
        self.logger.info(f"Discovering recordsets for zone {zone_id}...")
        return self._safe_list(self.conn.dns.recordsets, zone_id)
    
    def list_all_recordsets(self, zones: Iterable[Any]) -> Iterable[Any]:
        recordsets = []
        for zone in zones:
            recordsets.extend(self.list_recordsets(zone.id))
        return recordsets

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        zones = list(self.list_zones())
        recordsets = self.list_all_recordsets(zones)
        return {
            "zones": zones,
            "recordsets": recordsets
        }
