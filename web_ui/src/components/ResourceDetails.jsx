import React from 'react';
import { X } from 'lucide-react';

const ResourceDetails = ({ node, graph, onClose }) => {
  if (!node) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-white shadow-xl border-l border-gray-200 transform transition-transform duration-300 ease-in-out overflow-y-auto">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center sticky top-0 bg-white z-10">
        <h2 className="text-lg font-semibold text-gray-900 truncate pr-4">{node.label}</h2>
        <button onClick={onClose} className="p-1 hover:bg-gray-100 rounded-full">
          <X className="w-5 h-5 text-gray-500" />
        </button>
      </div>
      <div className="p-4 space-y-4">
        <div>
          <label className="text-xs font-medium text-gray-500 uppercase tracking-wider">Type</label>
          <div className="mt-1 text-sm text-gray-900 bg-gray-100 px-2 py-1 rounded inline-block">
            {node.type}
          </div>
        </div>
        <div>
          <label className="text-xs font-medium text-gray-500 uppercase tracking-wider">ID</label>
          <div className="mt-1 text-sm font-mono text-gray-600 break-all select-all">
            {node.id}
          </div>
        </div>
        {node.meta && (
          <div>
            <label className="text-xs font-medium text-gray-500 uppercase tracking-wider">Metadata</label>
            <div className="mt-2 bg-gray-50 rounded-md p-3 overflow-x-auto">
              <pre className="text-xs text-gray-700 font-mono">
                {JSON.stringify(node.meta, null, 2)}
              </pre>
            </div>
          </div>
        )}

        {/* Related Resources */}
        {graph && (
          <div>
             <label className="text-xs font-medium text-gray-500 uppercase tracking-wider">Related Resources</label>
             <div className="mt-2 space-y-2">
               {graph.edges
                 .filter(e => e.from === node.id || e.to === node.id)
                 .map((e, i) => {
                   const isSource = e.from === node.id;
                   const otherId = isSource ? e.to : e.from;
                   const otherNode = graph.nodes.find(n => n.id === otherId);
                   const relation = e.type || (isSource ? '->' : '<-');
                   
                   return (
                     <div key={i} className="flex items-center text-sm bg-gray-50 p-2 rounded border border-gray-100">
                       <span className="text-gray-500 text-xs mr-2 bg-gray-200 px-1 rounded">{relation}</span>
                       <span className="font-medium text-gray-700 truncate" title={otherNode?.label || otherId}>
                         {otherNode?.label || otherId}
                       </span>
                       <span className="ml-auto text-xs text-gray-400 uppercase">{otherNode?.type}</span>
                     </div>
                   );
                 })}
                 {graph.edges.filter(e => e.from === node.id || e.to === node.id).length === 0 && (
                   <div className="text-sm text-gray-400 italic">No related resources found</div>
                 )}
             </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResourceDetails;
