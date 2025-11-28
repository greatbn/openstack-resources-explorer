import React, { useRef, useEffect, useState, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const ResourceGraph = ({ graph, onSelect, selectedId }) => {
  const fgRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const containerRef = useRef();

  useEffect(() => {
    if (containerRef.current) {
      const { clientWidth, clientHeight } = containerRef.current;
      setDimensions({ width: clientWidth, height: clientHeight });
    }
    
    // Resize observer
    const ro = new ResizeObserver(entries => {
      for (let entry of entries) {
        setDimensions({ width: entry.contentRect.width, height: entry.contentRect.height });
      }
    });
    
    if (containerRef.current) {
      ro.observe(containerRef.current);
    }
    
    return () => ro.disconnect();
  }, []);

  // Prepare graph data
  const data = React.useMemo(() => {
    if (!graph) return { nodes: [], links: [] };
    
    // If no selection, return full graph (or maybe empty if desired, but full is better for exploration)
    if (!selectedId) {
        const nodes = graph.nodes.map(n => ({ ...n, val: 1 }));
        const links = graph.edges.map(e => ({ 
          source: e.from, 
          target: e.to,
          type: e.type
        }));
        return { nodes, links };
    }

    // BFS/Traversal to find related nodes
    const relatedNodeIds = new Set([selectedId]);
    const relatedLinks = [];

    // Helper to add neighbors
    const addNeighbors = (nodeId, depth = 1) => {
        if (depth <= 0) return;
        
        graph.edges.forEach(e => {
            if (e.from === nodeId) {
                if (!relatedNodeIds.has(e.to)) {
                    relatedNodeIds.add(e.to);
                    // If the neighbor is a port, go deeper to find SGs
                    const neighborNode = graph.nodes.find(n => n.id === e.to);
                    if (neighborNode && neighborNode.type === 'port') {
                        addNeighbors(e.to, depth - 1);
                    }
                }
                relatedLinks.push({ source: e.from, target: e.to, type: e.type });
            } else if (e.to === nodeId) {
                if (!relatedNodeIds.has(e.from)) {
                    relatedNodeIds.add(e.from);
                    // If the neighbor is a port, go deeper
                    const neighborNode = graph.nodes.find(n => n.id === e.from);
                    if (neighborNode && neighborNode.type === 'port') {
                        addNeighbors(e.from, depth - 1);
                    }
                }
                relatedLinks.push({ source: e.from, target: e.to, type: e.type });
            }
        });
    };

    // Start traversal
    // For Server, we want depth 2 (Server -> Port -> SG)
    // For others, maybe depth 1 is enough?
    // Let's use a modified logic:
    // 1. Add all direct neighbors.
    // 2. If a neighbor is a PORT, add its neighbors (SG, Network).
    
    graph.edges.forEach(e => {
        let neighborId = null;
        if (e.from === selectedId) neighborId = e.to;
        else if (e.to === selectedId) neighborId = e.from;

        if (neighborId) {
            relatedNodeIds.add(neighborId);
            relatedLinks.push({ source: e.from, target: e.to, type: e.type });

            // Check if neighbor is a port
            const neighbor = graph.nodes.find(n => n.id === neighborId);
            if (neighbor && neighbor.type === 'port') {
                // Add neighbors of this port
                graph.edges.forEach(e2 => {
                    if (e2.from === neighborId && e2.to !== selectedId) {
                        relatedNodeIds.add(e2.to);
                        relatedLinks.push({ source: e2.from, target: e2.to, type: e2.type });
                    } else if (e2.to === neighborId && e2.from !== selectedId) {
                        relatedNodeIds.add(e2.from);
                        relatedLinks.push({ source: e2.from, target: e2.to, type: e2.type });
                    }
                });
            }
        }
    });

    const nodes = graph.nodes
        .filter(n => relatedNodeIds.has(n.id))
        .map(n => ({ ...n, val: n.id === selectedId ? 3 : 1 }));
        
    // Filter links to only include those between visible nodes
    const finalLinks = relatedLinks.filter(l => relatedNodeIds.has(l.source) && relatedNodeIds.has(l.target));
    
    // Remove duplicates from links
    const uniqueLinks = [];
    const linkSet = new Set();
    finalLinks.forEach(l => {
        const key = `${l.source}-${l.target}-${l.type}`;
        if (!linkSet.has(key)) {
            linkSet.add(key);
            uniqueLinks.push(l);
        }
    });

    return { nodes, links: uniqueLinks };
  }, [graph, selectedId]);

  // Focus on selected node
  useEffect(() => {
    if (selectedId && fgRef.current) {
      // Small delay to allow graph to layout
      setTimeout(() => {
          const node = data.nodes.find(n => n.id === selectedId);
          if (node) {
            fgRef.current.centerAt(node.x, node.y, 1000);
            fgRef.current.zoom(4, 2000);
          }
      }, 100);
    }
  }, [selectedId, data]);

  const handleNodeClick = useCallback(node => {
    if (onSelect) {
      onSelect(node);
    }
  }, [onSelect]);

  const getNodeColor = (node) => {
    if (node.id === selectedId) return '#2563eb'; // Blue-600
    switch (node.type) {
      case 'server': return '#ef4444'; // Red-500
      case 'volume': return '#f59e0b'; // Amber-500
      case 'network': return '#10b981'; // Emerald-500
      case 'port': return '#6366f1'; // Indigo-500
      case 'router': return '#8b5cf6'; // Violet-500
      default: return '#9ca3af'; // Gray-400
    }
  };

  return (
    <div ref={containerRef} className="w-full h-full bg-gray-50">
      <ForceGraph2D
        ref={fgRef}
        width={dimensions.width}
        height={dimensions.height}
        graphData={data}
        nodeLabel="label"
        nodeColor={getNodeColor}
        nodeRelSize={6}
        linkColor={() => '#d1d5db'} // Gray-300
        onNodeClick={handleNodeClick}
        cooldownTicks={100}
        d3AlphaDecay={0.02}
        d3VelocityDecay={0.3}
      />
    </div>
  );
};

export default ResourceGraph;
