from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class NetworkDiscovery(DiscoveryBase):
    def list_networks(self) -> Iterable[Any]:
        self.logger.info("Discovering networks...")
        return self._safe_list(self.conn.network.networks, project_id=self.project_id)

    def list_subnets(self) -> Iterable[Any]:
        self.logger.info("Discovering subnets...")
        return self._safe_list(self.conn.network.subnets, project_id=self.project_id)

    def list_ports(self) -> Iterable[Any]:
        self.logger.info("Discovering ports...")
        return self._safe_list(self.conn.network.ports, project_id=self.project_id)

    def list_routers(self) -> Iterable[Any]:
        self.logger.info("Discovering routers...")
        return self._safe_list(self.conn.network.routers, project_id=self.project_id)

    def list_security_groups(self) -> Iterable[Any]:
        self.logger.info("Discovering security groups...")
        return self._safe_list(self.conn.network.security_groups, project_id=self.project_id)
    
    def list_floating_ips(self) -> Iterable[Any]:
        self.logger.info("Discovering floating IPs...")
        return self._safe_list(self.conn.network.ips, project_id=self.project_id)

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        return {
            "networks": self.list_networks(),
            "subnets": self.list_subnets(),
            "ports": self.list_ports(),
            "routers": self.list_routers(),
            "security_groups": self.list_security_groups(),
            "floating_ips": self.list_floating_ips()
        }
