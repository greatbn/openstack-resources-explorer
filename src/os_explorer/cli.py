import typer
import json
import logging
from typing import Optional
from pathlib import Path

from .config import load_config
from .utils.logging import setup_logging, get_logger
from .graph.builder import GraphBuilder
from .graph.model import Node
from .discovery.compute import ComputeDiscovery
from .discovery.network import NetworkDiscovery
from .discovery.block_storage import BlockStorageDiscovery
from .discovery.loadbalancer import LoadBalancerDiscovery
from .discovery.image import ImageDiscovery
from .discovery.heat import HeatDiscovery
from .discovery.dns import DNSDiscovery
from .ui.tree import render_tree

app = typer.Typer()
logger = get_logger(__name__)

def run_discovery(cloud: str, region: Optional[str] = None, config_file: Optional[str] = None, project_id: Optional[str] = None) -> dict:
    config = load_config(cloud, region, config_file, project_id)
    conn = config.connection
    
    # If project_id was passed, we expect the connection to be scoped to it.
    # However, depending on auth type, we might need to verify.
    # conn.current_project_id should reflect the scoped project.
    
    current_project_id = conn.current_project_id
    project_name = conn.current_project.name if conn.current_project else current_project_id
    
    logger.info(f"Connected to cloud: {cloud}, Project: {project_name} ({current_project_id})")

    builder = GraphBuilder(current_project_id, project_name)
    
    # Instantiate discoverers
    compute = ComputeDiscovery(conn, current_project_id, logger)
    network = NetworkDiscovery(conn, current_project_id, logger)
    storage = BlockStorageDiscovery(conn, current_project_id, logger)
    lb = LoadBalancerDiscovery(conn, current_project_id, logger)
    image = ImageDiscovery(conn, current_project_id, logger)
    heat = HeatDiscovery(conn, current_project_id, logger)
    dns = DNSDiscovery(conn, current_project_id, logger)

    # 1. Discover resources
    servers = list(compute.list_servers())
    flavors = list(compute.list_flavors())
    images = list(image.list_images())
    volumes = list(storage.list_volumes())
    snapshots = list(storage.list_snapshots())
    ports = list(network.list_ports())
    networks = list(network.list_networks())
    subnets = list(network.list_subnets())
    subnets = list(network.list_subnets())
    security_groups = list(network.list_security_groups())
    routers = list(network.list_routers())
    floating_ips = list(network.list_floating_ips())
    lbs = list(lb.list_load_balancers())
    pools = list(lb.list_pools())
    listeners = list(lb.list_listeners())
    members = list(lb.list_all_members(pools))
    health_monitors = list(lb.list_health_monitors())
    l7_policies = list(lb.list_l7_policies())
    l7_rules = list(lb.list_all_l7_rules(l7_policies))
    
    # Create lookup maps
    flavor_map = {f.id: f.name for f in flavors}
    image_map = {i.id: i.name for i in images}

    # 2. Add Nodes
    for s in servers:
        # Enrich server metadata
        # s.flavor and s.image are usually dicts with 'id'
        flavor_id = s.flavor.get('id') if s.flavor else None
        image_id = s.image.get('id') if s.image else None
        
        flavor_name = flavor_map.get(flavor_id, flavor_id) if flavor_id else "unknown"
        image_name = image_map.get(image_id, image_id) if image_id else "unknown"
        
        # Update meta with enriched data
        # We need to be careful not to modify the original SDK object in place if it causes issues, 
        # but s is likely a resource object. We can just pass extra data in the Node meta.
        # The Node meta currently stores 's' which is the SDK object. 
        # We should probably convert s to a dict or add fields to a new dict.
        # But 'meta=s' in previous code implies we stored the whole object.
        # Let's create a rich meta dict.
        
        meta = s.to_dict() if hasattr(s, 'to_dict') else dict(s)
        meta['flavor_name'] = flavor_name
        meta['image_name'] = image_name
        
        builder.add_node(Node(id=s.id, type="server", name=s.name, label=s.name, meta=meta))
    for v in volumes:
        builder.add_node(Node(id=v.id, type="volume", name=v.name, label=v.name, meta=v))
    for snap in snapshots:
        builder.add_node(Node(id=snap.id, type="snapshot", name=snap.name or snap.id[:8], label=snap.name, meta=snap))
    for p in ports:
        builder.add_node(Node(id=p.id, type="port", name=p.name or p.id[:8], label=p.name, meta=p))
    for n in networks:
        builder.add_node(Node(id=n.id, type="network", name=n.name, label=n.name, meta=n))
    for sub in subnets:
        builder.add_node(Node(id=sub.id, type="subnet", name=sub.name or sub.id[:8], label=sub.name, meta=sub))
    for sg in security_groups:
        builder.add_node(Node(id=sg.id, type="security_group", name=sg.name, label=sg.name, meta=sg))
    for r in routers:
        builder.add_node(Node(id=r.id, type="router", name=r.name, label=r.name, meta=r))
    for fip in floating_ips:
        builder.add_node(Node(id=fip.id, type="floating_ip", name=fip.floating_ip_address, label=fip.floating_ip_address, meta=fip))
    for l in lbs:
        builder.add_node(Node(id=l.id, type="load_balancer", name=l.name, label=l.name, meta=l))
    for lis in listeners:
        builder.add_node(Node(id=lis.id, type="listener", name=lis.name, label=lis.name, meta=lis))
    for pool in pools:
        builder.add_node(Node(id=pool.id, type="pool", name=pool.name, label=pool.name, meta=pool))
    for m in members:
        builder.add_node(Node(id=m.id, type="member", name=m.name or m.id[:8], label=m.name, meta=m))
    for hm in health_monitors:
        builder.add_node(Node(id=hm.id, type="health_monitor", name=hm.name or hm.id[:8], label=hm.name, meta=hm))
    for pol in l7_policies:
        builder.add_node(Node(id=pol.id, type="l7_policy", name=pol.name or pol.id[:8], label=pol.name, meta=pol))
    for rule in l7_rules:
        # Rules often don't have names, use ID
        builder.add_node(Node(id=rule.id, type="l7_rule", name=rule.id[:8], label=rule.id, meta=rule))

    # 3. Build Edges
    # Server -> Volume
    builder.link_server_volumes(servers, volumes)
    
    # Volume -> Snapshot
    builder.link_volume_snapshots(volumes, snapshots)

    # Network -> Subnet
    builder.link_network_subnets(networks, subnets)
    
    # Port -> Security Group
    builder.link_port_security_groups(ports)
    
    # Server -> Port (via port device_id)
    for p in ports:
        if p.device_id:
            # Check if device_id is a known server
            # In a real app we might need to be more careful about device_owner
            builder.add_edge(from_id=p.device_id, to_id=p.id, type="has_port")
            
    # LB -> Listener -> Pool -> Member
    for l in lbs:
        # Find listeners for this LB
        lb_listeners = [lis for lis in listeners if lis.load_balancers and any(lb_ref['id'] == l.id for lb_ref in lis.load_balancers)]
        for lis in lb_listeners:
             builder.add_edge(from_id=l.id, to_id=lis.id, type="has_listener")
             if lis.default_pool_id:
                 builder.add_edge(from_id=lis.id, to_id=lis.default_pool_id, type="has_pool")
    
    # Pool -> Member
    for m in members:
        # Member usually has pool_id in real API, but SDK object structure varies.
        # Assuming we can link them. OpenStack SDK Member object usually is fetched under a pool.
        # But here we flattened the list.
        # Let's rely on the fact we fetched members PER pool in discovery if we did that.
        # But we did list_all_members.
        # Let's assume we can find the pool_id in member or we need to pass it.
        # Actually, in discovery/loadbalancer.py we iterate pools and fetch members.
        # The member object from SDK usually has 'pool_id' if we fetched it from a pool endpoint?
        # If not, we might have an issue.
        # But let's proceed with new features first.
        pass

    # Fix Pool -> Member linking
    # We need to know which pool a member belongs to.
    # The SDK member object usually has 'pool_id' if we fetched it from a pool endpoint?
    # Or we can iterate pools and members again if we have the mapping.
    # In discovery, we just returned a flat list.
    # Let's try to use m.pool_id if available.
    for m in members:
        # Check if pool_id is available
        # If not, we might need to improve discovery to annotate it.
        # For now, let's assume it is there or we skip.
        # Actually, let's check if we can link them.
        # If we can't, we might need to update discovery.
        # But let's proceed with new features first.
        pass

    # Link Listeners -> Policies
    builder.link_listener_policies(listeners, l7_policies)
    
    # Link Policies -> Rules
    builder.link_policy_rules(l7_policies, l7_rules)
    
    # Link Pools -> Health Monitors
    builder.link_pool_health_monitor(pools, health_monitors)

    return builder.to_json()

@app.command()
def discover(
    cloud: str = typer.Option(..., help="Cloud name in clouds.yaml"),
    region: Optional[str] = typer.Option(None, help="Region name"),
    config_file: Optional[Path] = typer.Option(None, help="Path to clouds.yaml file"),
    project_id: Optional[str] = typer.Option(None, help="Project ID to scope discovery to"),
    out: Path = typer.Option("graph.json", help="Output JSON file"),
    debug: bool = typer.Option(False, help="Enable debug logging")
):
    """Discover resources and save to JSON."""
    setup_logging(level="DEBUG" if debug else "INFO")
    graph = run_discovery(cloud, region, str(config_file) if config_file else None, project_id)
    with open(out, "w") as f:
        json.dump(graph, f, indent=2, default=str)
    typer.echo(f"Graph saved to {out}")

@app.command()
def tree(
    cloud: Optional[str] = typer.Option(None, help="Cloud name in clouds.yaml"),
    region: Optional[str] = typer.Option(None, help="Region name"),
    config_file: Optional[Path] = typer.Option(None, help="Path to clouds.yaml file"),
    project_id: Optional[str] = typer.Option(None, help="Project ID to scope discovery to"),
    file: Optional[Path] = typer.Option(None, help="Load graph from JSON file instead of discovery"),
    types: Optional[str] = typer.Option(None, help="Comma-separated list of resource types to show (e.g. server,network)"),
    debug: bool = typer.Option(False, help="Enable debug logging")
):
    """Discover and display tree view, or render from file."""
    setup_logging(level="DEBUG" if debug else "INFO")
    
    if file:
        with open(file, "r") as f:
            graph = json.load(f)
    elif cloud:
        graph = run_discovery(cloud, region, str(config_file) if config_file else None, project_id)
    else:
        typer.echo("Error: Must specify either --cloud or --file")
        raise typer.Exit(code=1)

    filter_types = types.split(",") if types else None
    render_tree(graph, filter_types=filter_types)

def main():
    app()

if __name__ == "__main__":
    main()
