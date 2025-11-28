import React, { useMemo, useState } from 'react';
import { HardDrive, Network, Shield, Globe, Server, Box, ChevronDown, ChevronRight } from 'lucide-react';

const RelationCard = ({ title, icon: Icon, children }) => (
  <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden mb-4">
    <div className="bg-gray-50 px-4 py-2 border-b border-gray-200 flex items-center">
      {Icon && <Icon className="w-4 h-4 mr-2 text-gray-500" />}
      <h3 className="text-sm font-medium text-gray-700">{title}</h3>
    </div>
    <div className="p-4">
      {children}
    </div>
  </div>
);

const ResourceItem = ({ node, subtext }) => (
  <div className="flex items-start py-2 border-b border-gray-100 last:border-0">
    <div className="flex-1 min-w-0">
      <p className="text-sm font-medium text-gray-900 truncate">
        {node.label || node.name || node.id}
      </p>
      {subtext && (
        <p className="text-xs text-gray-500 truncate">{subtext}</p>
      )}
      <p className="text-xs text-gray-400 font-mono truncate">{node.id}</p>
    </div>
    <div className="ml-2">
       <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
         {node.type}
       </span>
    </div>
  </div>
);

const SecurityGroupRules = ({ node }) => {
  const [expanded, setExpanded] = useState(false);
  const rules = node.meta?.security_group_rules || [];

  if (rules.length === 0) return (
    <span className="text-xs bg-white border border-gray-200 px-1.5 py-0.5 rounded text-gray-700" title={node.id}>
        {node.label}
    </span>
  );

  return (
    <div className="w-full mt-1">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="flex items-center text-xs bg-white border border-gray-200 px-1.5 py-0.5 rounded text-gray-700 hover:bg-gray-50 w-full text-left"
      >
        {expanded ? <ChevronDown className="w-3 h-3 mr-1" /> : <ChevronRight className="w-3 h-3 mr-1" />}
        <span className="font-medium">{node.label}</span>
        <span className="ml-auto text-gray-400 text-[10px]">{rules.length} rules</span>
      </button>
      
      {expanded && (
        <div className="mt-2 overflow-x-auto">
          <table className="min-w-full text-xs text-left text-gray-500 border border-gray-200">
            <thead className="bg-gray-50 text-gray-700 font-medium">
              <tr>
                <th className="px-2 py-1 border-b">Direction</th>
                <th className="px-2 py-1 border-b">Proto</th>
                <th className="px-2 py-1 border-b">Port Range</th>
                <th className="px-2 py-1 border-b">Remote</th>
                <th className="px-2 py-1 border-b">Ethertype</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {rules.map((rule, idx) => (
                <tr key={rule.id || idx} className="hover:bg-gray-50">
                  <td className="px-2 py-1">{rule.direction}</td>
                  <td className="px-2 py-1 uppercase">{rule.protocol || 'Any'}</td>
                  <td className="px-2 py-1">
                    {rule.port_range_min === rule.port_range_max 
                      ? (rule.port_range_min || 'Any') 
                      : `${rule.port_range_min}-${rule.port_range_max}`}
                  </td>
                  <td className="px-2 py-1">
                    {rule.remote_ip_prefix || rule.remote_group_id || 'Any'}
                  </td>
                  <td className="px-2 py-1">{rule.ethertype}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

const ResourceRelations = ({ node, graph }) => {
  const relations = useMemo(() => {
    if (!node || !graph) return null;

    const result = {
      volumes: [],
      ports: [],
      others: []
    };

    // Find direct neighbors
    const directNeighbors = [];
    graph.edges.forEach(e => {
      if (e.from === node.id) directNeighbors.push({ id: e.to, type: e.type });
      else if (e.to === node.id) directNeighbors.push({ id: e.from, type: e.type });
    });

    directNeighbors.forEach(neighbor => {
      const neighborNode = graph.nodes.find(n => n.id === neighbor.id);
      if (!neighborNode) return;

      if (neighborNode.type === 'volume') {
        result.volumes.push(neighborNode);
      } else if (neighborNode.type === 'port') {
        // Find things attached to this port (SGs, IPs)
        const portRelations = {
          node: neighborNode,
          securityGroups: [],
          ips: []
        };
        
        graph.edges.forEach(e => {
            let subNeighborId = null;
            if (e.from === neighborNode.id && e.to !== node.id) subNeighborId = e.to;
            else if (e.to === neighborNode.id && e.from !== node.id) subNeighborId = e.from;
            
            if (subNeighborId) {
                const subNode = graph.nodes.find(n => n.id === subNeighborId);
                if (subNode) {
                    if (subNode.type === 'security_group') {
                        portRelations.securityGroups.push(subNode);
                    } else if (subNode.type === 'floating_ip') {
                        portRelations.ips.push(subNode);
                    }
                }
            }
        });
        result.ports.push(portRelations);
      } else {
        result.others.push(neighborNode);
      }
    });

    return result;
  }, [node, graph]);

  if (!node) return null;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 flex items-center">
          <Server className="w-6 h-6 mr-2 text-blue-600" />
          {node.label}
        </h1>
        <p className="text-gray-500 font-mono text-sm mt-1">{node.id}</p>
      </div>

      {relations.volumes.length > 0 && (
        <RelationCard title="Attached Volumes" icon={HardDrive}>
          <div className="divide-y divide-gray-100">
            {relations.volumes.map(vol => (
              <ResourceItem 
                key={vol.id} 
                node={vol} 
                subtext={`Size: ${vol.meta?.size}GB | Status: ${vol.meta?.status}`} 
              />
            ))}
          </div>
        </RelationCard>
      )}

      {relations.ports.length > 0 && (
        <RelationCard title="Network Interfaces" icon={Network}>
          <div className="space-y-4">
            {relations.ports.map(item => (
              <div key={item.node.id} className="bg-gray-50 rounded p-3 border border-gray-100">
                <div className="flex justify-between items-start mb-2">
                    <div>
                        <p className="text-sm font-medium text-gray-900">Port: {item.node.label || item.node.id.substring(0,8)}</p>
                        <p className="text-xs text-gray-500 font-mono">{item.node.meta?.mac_address || item.node.id}</p>
                        {item.node.meta?.fixed_ips && item.node.meta.fixed_ips.map((ip, idx) => (
                             <p key={idx} className="text-xs text-blue-600 font-medium">{ip.ip_address}</p>
                        ))}
                    </div>
                    <span className="text-xs bg-white border border-gray-200 px-2 py-0.5 rounded text-gray-600">
                        {item.node.meta?.status || 'ACTIVE'}
                    </span>
                </div>

                {item.securityGroups.length > 0 && (
                    <div className="mt-2 pl-2 border-l-2 border-gray-200">
                        <p className="text-xs font-semibold text-gray-500 mb-1 flex items-center">
                            <Shield className="w-3 h-3 mr-1" /> Security Groups
                        </p>
                        <div className="space-y-1">
                            {item.securityGroups.map(sg => (
                                <SecurityGroupRules key={sg.id} node={sg} />
                            ))}
                        </div>
                    </div>
                )}
                
                {item.ips.length > 0 && (
                    <div className="mt-2 pl-2 border-l-2 border-gray-200">
                         <p className="text-xs font-semibold text-gray-500 mb-1 flex items-center">
                            <Globe className="w-3 h-3 mr-1" /> Floating IPs
                        </p>
                        {item.ips.map(fip => (
                            <span key={fip.id} className="text-xs bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded border border-blue-100">
                                {fip.floating_ip_address}
                            </span>
                        ))}
                    </div>
                )}
              </div>
            ))}
          </div>
        </RelationCard>
      )}

      {relations.others.length > 0 && (
        <RelationCard title="Other Relations" icon={Box}>
          <div className="divide-y divide-gray-100">
            {relations.others.map(other => (
              <ResourceItem key={other.id} node={other} />
            ))}
          </div>
        </RelationCard>
      )}
      
      {relations.volumes.length === 0 && relations.ports.length === 0 && relations.others.length === 0 && (
          <div className="text-center py-8 text-gray-500">
              No related resources found.
          </div>
      )}
    </div>
  );
};

export default ResourceRelations;
