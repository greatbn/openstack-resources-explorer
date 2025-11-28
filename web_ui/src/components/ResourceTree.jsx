import React, { useState, useMemo } from 'react';
import { ChevronRight, ChevronDown, Server, HardDrive, Network, Globe, Box, Activity } from 'lucide-react';

const TypeIcon = ({ type }) => {
  switch (type) {
    case 'server': return <Server className="w-4 h-4" />;
    case 'volume': return <HardDrive className="w-4 h-4" />;
    case 'network': return <Network className="w-4 h-4" />;
    case 'floating_ip': return <Globe className="w-4 h-4" />;
    case 'load_balancer': return <Activity className="w-4 h-4" />;
    default: return <Box className="w-4 h-4" />;
  }
};

const ResourceGroup = ({ type, nodes, onSelect, selectedId }) => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className="mb-2">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="flex items-center w-full px-2 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
      >
        {expanded ? <ChevronDown className="w-4 h-4 mr-1 text-gray-400" /> : <ChevronRight className="w-4 h-4 mr-1 text-gray-400" />}
        <span className="capitalize">{type.replace('_', ' ')}</span>
        <span className="ml-auto text-xs text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded-full">{nodes.length}</span>
      </button>
      
      {expanded && (
        <div className="ml-4 mt-1 space-y-0.5 border-l border-gray-200 pl-2">
          {nodes.map(node => (
            <button
              key={node.id}
              onClick={() => onSelect(node)}
              className={`flex items-center w-full px-2 py-1.5 text-sm rounded-md transition-colors text-left group ${
                selectedId === node.id 
                  ? 'bg-blue-50 text-blue-700' 
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              }`}
            >
              <span className={`mr-2 ${selectedId === node.id ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'}`}>
                <TypeIcon type={type} />
              </span>
              <span className="truncate">{node.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

const ResourceTree = ({ graph, onSelect, selectedId }) => {
  const groupedNodes = useMemo(() => {
    if (!graph || !graph.nodes) return {};
    return graph.nodes.reduce((acc, node) => {
      if (!acc[node.type]) acc[node.type] = [];
      acc[node.type].push(node);
      return acc;
    }, {});
  }, [graph]);

  if (!graph) return <div className="p-4 text-gray-500 text-sm">No data available</div>;

  return (
    <div className="p-4 space-y-4">
      {Object.entries(groupedNodes).map(([type, nodes]) => (
        <ResourceGroup 
          key={type} 
          type={type} 
          nodes={nodes} 
          onSelect={onSelect}
          selectedId={selectedId}
        />
      ))}
    </div>
  );
};

export default ResourceTree;
