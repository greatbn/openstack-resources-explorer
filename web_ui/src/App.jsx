import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Cloud, RefreshCw, AlertCircle } from 'lucide-react';
import ResourceTree from './components/ResourceTree';
import ResourceRelations from './components/ResourceRelations';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [clouds, setClouds] = useState([]);
  const [selectedCloud, setSelectedCloud] = useState('');
  const [graph, setGraph] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  useEffect(() => {
    fetchClouds();
  }, []);

  const fetchClouds = async () => {
    try {
      const res = await axios.get(`${API_BASE}/clouds`);
      setClouds(res.data);
      if (res.data.length > 0) {
        setSelectedCloud(res.data[0]);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to load clouds. Is the backend running?');
    }
  };

  const fetchGraph = async () => {
    if (!selectedCloud) return;
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`${API_BASE}/graph`, {
        params: { cloud: selectedCloud }
      });
      setGraph(res.data);
    } catch (err) {
      console.error(err);
      setError(`Failed to load resources for ${selectedCloud}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCloud) {
      fetchGraph();
    }
  }, [selectedCloud]);

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col flex-shrink-0">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-xl font-bold text-gray-900 flex items-center">
              <Cloud className="w-6 h-6 mr-2 text-blue-600" />
              OS Explorer
            </h1>
          </div>
          
          <div className="space-y-2">
            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Select Cloud</label>
            <div className="flex space-x-2">
              <select 
                value={selectedCloud}
                onChange={(e) => setSelectedCloud(e.target.value)}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
              >
                {clouds.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
              <button 
                onClick={fetchGraph} 
                disabled={loading}
                className="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
                title="Refresh"
              >
                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto">
          {error ? (
            <div className="p-4 text-red-600 text-sm flex items-start bg-red-50 m-4 rounded-md">
              <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
              {error}
            </div>
          ) : (
            <ResourceTree 
              graph={graph} 
              onSelect={setSelectedNode} 
              selectedId={selectedNode?.id}
            />
          )}
        </div>
      </div>

      {/* Main Content / Details */}
      <div className="flex-1 flex flex-col min-w-0 bg-gray-50 relative overflow-y-auto">
        {selectedNode ? (
          <ResourceRelations 
            node={selectedNode} 
            graph={graph} 
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400 flex-col">
            <Cloud className="w-16 h-16 mb-4 text-gray-300" />
            <p className="text-lg">Select a resource to view details</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
