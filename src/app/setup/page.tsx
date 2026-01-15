'use client';

import { useState } from 'react';

export default function SetupPage() {
  const [status, setStatus] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const checkSetupStatus = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/setup');
      const data = await response.json();
      setStatus(JSON.stringify(data, null, 2));
    } catch (error) {
      setStatus(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const initializeDatabase = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/setup', {
        method: 'POST',
      });
      const data = await response.json();
      setStatus(JSON.stringify(data, null, 2));
    } catch (error) {
      setStatus(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">Database Setup</h1>
            <p className="text-gray-600">
              Initialize your database with default users and settings
            </p>
          </div>
          
          <div className="space-y-4">
            <div className="flex gap-4">
              <button 
                onClick={checkSetupStatus} 
                disabled={loading}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Check Status'}
              </button>
              <button 
                onClick={initializeDatabase} 
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Loading...' : 'Initialize Database'}
              </button>
            </div>
            
            {status && (
              <div className="mt-4 p-4 bg-gray-100 rounded-md">
                <h3 className="font-semibold mb-2">Result:</h3>
                <pre className="whitespace-pre-wrap text-sm text-gray-800">{status}</pre>
              </div>
            )}
            
            <div className="mt-6 p-4 border rounded-md bg-blue-50">
              <h3 className="font-semibold mb-2">Default Users:</h3>
              <ul className="text-sm space-y-1">
                <li><strong>Admin:</strong> admin@salesportal.com / admin123</li>
                <li><strong>Agent:</strong> agent@salesportal.com / agent123</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}