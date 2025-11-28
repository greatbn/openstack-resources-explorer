from typing import Iterable, Dict, Any
from .base import DiscoveryBase

class LoadBalancerDiscovery(DiscoveryBase):
    def list_load_balancers(self) -> Iterable[Any]:
        self.logger.info("Discovering load balancers...")
        return self._safe_list(self.conn.load_balancer.load_balancers, project_id=self.project_id)

    def list_listeners(self) -> Iterable[Any]:
        self.logger.info("Discovering listeners...")
        return self._safe_list(self.conn.load_balancer.listeners, project_id=self.project_id)

    def list_pools(self) -> Iterable[Any]:
        self.logger.info("Discovering pools...")
        return self._safe_list(self.conn.load_balancer.pools, project_id=self.project_id)

    def list_members(self, pool_id: str) -> Iterable[Any]:
        # Members are usually sub-resources of pools
        self.logger.info(f"Discovering members for pool {pool_id}...")
        return self._safe_list(self.conn.load_balancer.members, pool_id)
    
    def list_all_members(self, pools: Iterable[Any]) -> Iterable[Any]:
        members = []
        for pool in pools:
            members.extend(self.list_members(pool.id))
        return members

    def list_l7_policies(self) -> Iterable[Any]:
        self.logger.info("Discovering L7 policies...")
        return self._safe_list(self.conn.load_balancer.l7_policies, project_id=self.project_id)

    def list_l7_rules(self, policy_id: str) -> Iterable[Any]:
        self.logger.info(f"Discovering rules for policy {policy_id}...")
        return self._safe_list(self.conn.load_balancer.l7_rules, policy_id)

    def list_all_l7_rules(self, policies: Iterable[Any]) -> Iterable[Any]:
        rules = []
        for policy in policies:
            rules.extend(self.list_l7_rules(policy.id))
        return rules

    def list_health_monitors(self) -> Iterable[Any]:
        self.logger.info("Discovering health monitors...")
        return self._safe_list(self.conn.load_balancer.health_monitors, project_id=self.project_id)

    def list_resources(self) -> Dict[str, Iterable[Any]]:
        lbs = list(self.list_load_balancers())
        pools = list(self.list_pools())
        # We need to fetch members for each pool
        members = self.list_all_members(pools)
        
        policies = list(self.list_l7_policies())
        rules = self.list_all_l7_rules(policies)
        
        return {
            "load_balancers": lbs,
            "listeners": self.list_listeners(),
            "pools": pools,
            "members": members,
            "health_monitors": self.list_health_monitors(),
            "l7_policies": policies,
            "l7_rules": rules
        }
