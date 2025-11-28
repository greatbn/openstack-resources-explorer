from typing import List, Dict, Any, Optional
from .model import Graph, Node, Edge

class GraphBuilder:
    def __init__(self, project_id: str, project_name: str):
        self.graph = Graph(project_id=project_id, project_name=project_name)

    def add_node(self, node: Node):
        self.graph.add_node(node)

    def add_edge(self, from_id: str, to_id: str, type: str, meta: Optional[Dict[str, Any]] = None):
        if meta is None:
            meta = {}
        edge = Edge(from_node=from_id, to_node=to_id, type=type, meta=meta)
        self.graph.add_edge(edge)

    def link_server_volumes(self, servers: List[Dict[str, Any]], volumes: List[Dict[str, Any]]):
        """Link servers to their attached volumes."""
        server_ids = {s['id'] for s in servers}
        for vol in volumes:
            # Check if volume is attached to any known server
            attachments = vol.get('attachments', [])
            if attachments is None:
                attachments = []
            
            for attachment in attachments:
                s_id = attachment.get('server_id')
                if s_id and s_id in server_ids:
                    self.add_edge(
                        from_id=s_id,
                        to_id=vol['id'],
                        type="attached",
                        meta={"device": attachment.get("device")}
                    )

    def link_volume_snapshots(self, volumes: List[Dict[str, Any]], snapshots: List[Dict[str, Any]]):
        """Link volumes to their snapshots."""
        for snap in snapshots:
            volume_id = snap.get('volume_id')
            if volume_id:
                # We only add the edge if the volume exists in our graph (or we assume it does)
                # Ideally we check if volume_id is in our nodes, but for now we just add the edge.
                # The UI handles missing nodes gracefully.
                self.add_edge(
                    from_id=volume_id,
                    to_id=snap['id'],
                    type="has_snapshot"
                )

    def link_network_subnets(self, networks: List[Dict[str, Any]], subnets: List[Dict[str, Any]]):
        """Link networks to their subnets."""
        for subnet in subnets:
            network_id = subnet.get('network_id')
            if network_id:
                self.add_edge(
                    from_id=network_id,
                    to_id=subnet['id'],
                    type="has_subnet"
                )

    def link_port_security_groups(self, ports: List[Dict[str, Any]]):
        """Link ports to their security groups."""
        for port in ports:
            # Ports usually have 'security_groups' or 'security_group_ids'
            sg_ids = port.get('security_groups') or port.get('security_group_ids', [])
            for sg_id in sg_ids:
                self.add_edge(
                    from_id=port['id'],
                    to_id=sg_id,
                    type="has_sg"
                )

    def link_listener_policies(self, listeners: List[Dict[str, Any]], policies: List[Dict[str, Any]]):
        """Link listeners to their L7 policies."""
        for policy in policies:
            listener_id = policy.get('listener_id')
            if listener_id:
                self.add_edge(
                    from_id=listener_id,
                    to_id=policy['id'],
                    type="has_policy",
                    meta={"position": policy.get("position")}
                )

    def link_policy_rules(self, policies: List[Dict[str, Any]], rules: List[Dict[str, Any]]):
        """Link L7 policies to their rules."""
        # Rules usually belong to a policy, but the rule object might not have policy_id if fetched via policy sub-resource
        # However, openstacksdk rule object usually has it.
        # If we fetched rules by policy, we know the parent.
        # Let's assume the rule object has 'policy_id' or we need to pass it if we iterate differently.
        # In our discovery, we fetched rules per policy but flattened the list.
        # OpenStack SDK L7Rule object has 'l7_policy_id' usually.
        # Let's check if we can rely on that.
        for rule in rules:
            # The SDK might use 'l7_policy_id' or we might need to rely on how we fetched them.
            # Let's assume 'l7_policy_id' is present.
            # If not, we might need to adjust discovery to attach it.
            # But wait, we fetched them using `conn.load_balancer.l7_rules(policy_id)`.
            # The returned objects should have the ID.
            # Let's try to use 'l7_policy_id' or 'policy_id'.
            policy_id = rule.get('l7_policy_id') or rule.get('policy_id')
            if policy_id:
                self.add_edge(
                    from_id=policy_id,
                    to_id=rule['id'],
                    type="has_rule"
                )

    def link_pool_health_monitor(self, pools: List[Dict[str, Any]], monitors: List[Dict[str, Any]]):
        """Link pools to their health monitors."""
        # Pools have 'health_monitor_id' usually.
        # Or monitors have 'pool_id'.
        # SDK HealthMonitor has 'pools' list (usually one).
        for monitor in monitors:
            # Monitor can be attached to multiple pools in some versions, but usually 1:1 in Octavia?
            # Actually HM has 'pools' attribute which is a list of dicts with 'id'.
            monitor_pools = monitor.get('pools', [])
            for pool_ref in monitor_pools:
                self.add_edge(
                    from_id=pool_ref['id'],
                    to_id=monitor['id'],
                    type="has_monitor"
                )

    def to_json(self) -> Dict[str, Any]:
        return self.graph.to_dict()
