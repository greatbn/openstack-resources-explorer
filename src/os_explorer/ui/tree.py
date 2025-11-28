from rich.tree import Tree
from rich.console import Console
from typing import Dict, Any, List, Optional

def find_node(graph_json: Dict[str, Any], node_id: str) -> Optional[Dict[str, Any]]:
    for node in graph_json.get('nodes', []):
        if node['id'] == node_id:
            return node
    return None

def render_tree(graph_json: Dict[str, Any], max_depth: int = 3, highlight: Optional[str] = None, filter_types: Optional[List[str]] = None) -> None:
    """Render tree to terminal using rich"""
    console = Console()
    project_name = graph_json.get('project_name', 'Unknown Project')
    root = Tree(f"[bold cyan]Project: {project_name}[/]")

    nodes = graph_json.get('nodes', [])
    edges = graph_json.get('edges', [])
    
    # Normalize filter_types
    if filter_types:
        filter_types = [t.lower() for t in filter_types]

    def should_show(resource_type: str) -> bool:
        if not filter_types:
            return True
        return resource_type.lower() in filter_types

    # Servers
    if should_show('server'):
        servers = [n for n in nodes if n['type'] == 'server']
        if servers:
            serv_branch = root.add(f"Servers ({len(servers)})")
            for s in servers:
                az = s['meta'].get('availability_zone', 'unknown-az')
                status = s['meta'].get('status', 'UNKNOWN')
                status_color = "green" if status == 'ACTIVE' else "red"
                
                s_node = serv_branch.add(f"[bold green]{s['name']}[/] ({s['id']}) [dim]AZ: {az}[/] [{status_color}]{status}[/]")
                
                # Detailed Info
                details = []
                if 'flavor_name' in s['meta']:
                    details.append(f"Flavor: {s['meta']['flavor_name']}")
                if 'image_name' in s['meta']:
                    details.append(f"Image: {s['meta']['image_name']}")
                if 'key_name' in s['meta'] and s['meta']['key_name']:
                    details.append(f"Key: {s['meta']['key_name']}")
                if 'created_at' in s['meta']:
                    details.append(f"Created: {s['meta']['created_at']}")
                
                if details:
                    s_node.add(f"[dim]{', '.join(details)}[/]")
                
                # Volumes
                vols = [e['to'] for e in edges if e['from'] == s['id'] and e['type'] == 'attached']
                if vols:
                    vbranch = s_node.add("Volumes:")
                    for vid in vols:
                        v = find_node(graph_json, vid)
                        if v:
                            size = v['meta'].get('size', '?') # OpenStack SDK uses 'size' usually, check discovery
                            v_type = v['meta'].get('volume_type', 'unknown-type')
                            name = v['name'] if v['name'] else v['id']
                            v_node = vbranch.add(f"{name} ({v['id']}) ({size}GB, {v_type})")
                            
                            # Snapshots
                            snaps = [e['to'] for e in edges if e['from'] == vid and e['type'] == 'has_snapshot']
                            if snaps:
                                snap_branch = v_node.add("Snapshots:")
                                for snap_id in snaps:
                                    snap = find_node(graph_json, snap_id)
                                    if snap:
                                        snap_size = snap['meta'].get('size', '?')
                                        snap_branch.add(f"{snap['name']} ({snap['id']}) ({snap_size}GB)")

                # Ports
                ports = [e['to'] for e in edges if e['from'] == s['id'] and e['type'] == 'has_port']
                if ports:
                    pbranch = s_node.add("Ports:")
                    for pid in ports:
                        p = find_node(graph_json, pid)
                        if p:
                            fixed_ips = p['meta'].get('fixed_ips', [])
                            ip_str = ", ".join([ip['ip_address'] for ip in fixed_ips]) if fixed_ips else "-"
                            pnode = pbranch.add(f"{p['name']} ({p['id']}) ({ip_str})")
                            
                            # Security Groups
                            sgs = [e['to'] for e in edges if e['from'] == pid and e['type'] == 'has_sg']
                            if sgs:
                                sg_branch = pnode.add("Security Groups:")
                                for sgid in sgs:
                                    sg = find_node(graph_json, sgid)
                                    if sg:
                                        sg_node = sg_branch.add(f"{sg['name']} ({sg['id']})")
                                        
                                        # Display Rules
                                        rules = sg['meta'].get('security_group_rules', [])
                                        if rules:
                                            rule_branch = sg_node.add("Rules:")
                                            for rule in rules:
                                                direction = rule.get('direction', 'unknown')
                                                protocol = rule.get('protocol', 'any')
                                                port_range_min = rule.get('port_range_min')
                                                port_range_max = rule.get('port_range_max')
                                                remote_ip = rule.get('remote_ip_prefix')
                                                remote_group = rule.get('remote_group_id')
                                                
                                                ports = "Any"
                                                if port_range_min and port_range_max:
                                                    if port_range_min == port_range_max:
                                                        ports = str(port_range_min)
                                                    else:
                                                        ports = f"{port_range_min}-{port_range_max}"
                                                elif port_range_min:
                                                    ports = str(port_range_min)
                                                
                                                remote = remote_ip if remote_ip else (f"Group: {remote_group}" if remote_group else "Any")
                                                
                                                rule_branch.add(f"{direction} {protocol} {ports} -> {remote}")

    # Networks
    if should_show('network'):
        networks = [n for n in nodes if n['type'] == 'network']
        if networks:
            net_branch = root.add(f"Networks ({len(networks)})")
            for n in networks:
                n_node = net_branch.add(f"{n['name']} ({n['id']})")
                
                # Subnets
                subnets = [e['to'] for e in edges if e['from'] == n['id'] and e['type'] == 'has_subnet']
                if subnets:
                    sub_branch = n_node.add("Subnets:")
                    for sub_id in subnets:
                        sub = find_node(graph_json, sub_id)
                        if sub:
                            cidr = sub['meta'].get('cidr', '?')
                            gateway = sub['meta'].get('gateway_ip', '?')
                            sub_branch.add(f"{sub['name']} ({sub['id']}) (CIDR: {cidr}, GW: {gateway})")

    # Load Balancers
    if should_show('load_balancer'):
        lbs = [n for n in nodes if n['type'] == 'load_balancer']
        if lbs:
            lb_branch = root.add(f"Load Balancers ({len(lbs)})")
            for lb in lbs:
                l_node = lb_branch.add(f"{lb['name']} ({lb['id']})")
                # Listeners
                listeners = [e['to'] for e in edges if e['from'] == lb['id'] and e['type'] == 'has_listener']
                if listeners:
                    lis_branch = l_node.add("Listeners:")
                    for lis_id in listeners:
                        lis = find_node(graph_json, lis_id)
                        if lis:
                            lis_node = lis_branch.add(f"{lis['name']} ({lis['id']}) ({lis['meta'].get('protocol', '?')}:{lis['meta'].get('protocol_port', '?')})")
                            
                            # L7 Policies
                            policies = [e['to'] for e in edges if e['from'] == lis_id and e['type'] == 'has_policy']
                            if policies:
                                pol_branch = lis_node.add("L7 Policies:")
                                for pol_id in policies:
                                    pol = find_node(graph_json, pol_id)
                                    if pol:
                                        pol_node = pol_branch.add(f"{pol['name']} ({pol['id']}) (Action: {pol['meta'].get('action', '?')})")
                                        
                                        # L7 Rules
                                        rules = [e['to'] for e in edges if e['from'] == pol_id and e['type'] == 'has_rule']
                                        if rules:
                                            rule_branch = pol_node.add("Rules:")
                                            for rule_id in rules:
                                                rule = find_node(graph_json, rule_id)
                                                if rule:
                                                    rule_type = rule['meta'].get('type', '?')
                                                    compare_type = rule['meta'].get('compare_type', '?')
                                                    value = rule['meta'].get('value', '?')
                                                    key = rule['meta'].get('key', '')
                                                    rule_branch.add(f"{rule_type} {compare_type} {key} {value} ({rule['id']})")

                            # Default Pool
                            pools = [e['to'] for e in edges if e['from'] == lis_id and e['type'] == 'has_pool']
                            if pools:
                                pool_branch = lis_node.add("Default Pool:")
                                for pool_id in pools:
                                    pool = find_node(graph_json, pool_id)
                                    if pool:
                                        p_node = pool_branch.add(f"{pool['name']} ({pool['id']}) ({pool['meta'].get('protocol', '?')})")
                                        
                                        # Health Monitor
                                        monitors = [e['to'] for e in edges if e['from'] == pool_id and e['type'] == 'has_monitor']
                                        if monitors:
                                            hm_branch = p_node.add("Health Monitor:")
                                            for hm_id in monitors:
                                                hm = find_node(graph_json, hm_id)
                                                if hm:
                                                    hm_type = hm['meta'].get('type', '?')
                                                    delay = hm['meta'].get('delay', '?')
                                                    max_retries = hm['meta'].get('max_retries', '?')
                                                    hm_branch.add(f"{hm['name']} ({hm['id']}) (Type: {hm_type}, Delay: {delay}s, Retries: {max_retries})")

                                        # Members
                                        members = [e['to'] for e in edges if e['from'] == pool_id and e['type'] == 'has_member']
                                        if members:
                                            m_branch = p_node.add("Members:")
                                            for mid in members:
                                                m = find_node(graph_json, mid)
                                                if m:
                                                    m_branch.add(f"{m['name']} ({m['id']}) ({m['meta'].get('address', '-')})")

    # Routers
    if should_show('router'):
        routers = [n for n in nodes if n['type'] == 'router']
        if routers:
            r_branch = root.add(f"Routers ({len(routers)})")
            for r in routers:
                status = r['meta'].get('status', 'UNKNOWN')
                status_color = "green" if status == 'ACTIVE' else "red"
                r_branch.add(f"{r['name']} ({r['id']}) [{status_color}]{status}[/]")

    # Floating IPs
    if should_show('floating_ip'):
        fips = [n for n in nodes if n['type'] == 'floating_ip']
        if fips:
            fip_branch = root.add(f"Floating IPs ({len(fips)})")
            for fip in fips:
                status = fip['meta'].get('status', 'UNKNOWN')
                status_color = "green" if status == 'ACTIVE' else "red"
                fixed_ip = fip['meta'].get('fixed_ip_address', '-')
                fip_branch.add(f"{fip['name']} ({fip['id']}) -> {fixed_ip} [{status_color}]{status}[/]")

    # Volumes (Top Level - Unattached Only)
    if should_show('volume'):
        # Find all volume IDs that are attached (target of 'attached' edge)
        attached_vol_ids = set()
        for e in edges:
            if e['type'] == 'attached':
                attached_vol_ids.add(e['to'])

        all_volumes = [n for n in nodes if n['type'] == 'volume']
        unattached_volumes = [v for v in all_volumes if v['id'] not in attached_vol_ids]
                
        if unattached_volumes:
            vol_branch = root.add(f"Volumes (Unattached) ({len(unattached_volumes)})")
            for v in unattached_volumes:
                status = v['meta'].get('status', 'UNKNOWN')
                status_color = "green" if status == 'available' or status == 'in-use' else "red"
                size = v['meta'].get('size', '?')
                v_type = v['meta'].get('volume_type', 'unknown-type')
                
                name = v['name'] if v['name'] else v['id']
                v_node = vol_branch.add(f"{name} ({v['id']}) ({size}GB, {v_type}) [{status_color}]{status}[/]")
                
                # Snapshots
                snaps = [e['to'] for e in edges if e['from'] == v['id'] and e['type'] == 'has_snapshot']
                if snaps:
                    snap_branch = v_node.add("Snapshots:")
                    for snap_id in snaps:
                        snap = find_node(graph_json, snap_id)
                        if snap:
                            snap_size = snap['meta'].get('size', '?')
                            snap_branch.add(f"{snap['name']} ({snap['id']}) ({snap_size}GB)")

    # Security Groups (Top Level)
    if should_show('security_group'):
        sgs = [n for n in nodes if n['type'] == 'security_group']
        if sgs:
            sg_branch = root.add(f"Security Groups ({len(sgs)})")
            for sg in sgs:
                sg_node = sg_branch.add(f"{sg['name']} ({sg['id']})")
                # Rules
                rules = sg['meta'].get('security_group_rules', [])
                if rules:
                    rule_branch = sg_node.add("Rules:")
                    for rule in rules:
                        direction = rule.get('direction', 'unknown')
                        protocol = rule.get('protocol', 'any')
                        port_range_min = rule.get('port_range_min')
                        port_range_max = rule.get('port_range_max')
                        remote_ip = rule.get('remote_ip_prefix')
                        remote_group = rule.get('remote_group_id')
                        
                        ports = "Any"
                        if port_range_min and port_range_max:
                            if port_range_min == port_range_max:
                                ports = str(port_range_min)
                            else:
                                ports = f"{port_range_min}-{port_range_max}"
                        elif port_range_min:
                            ports = str(port_range_min)
                        
                        remote = remote_ip if remote_ip else (f"Group: {remote_group}" if remote_group else "Any")
                        
                        rule_branch.add(f"{direction} {protocol} {ports} -> {remote}")
    console.print(root)
