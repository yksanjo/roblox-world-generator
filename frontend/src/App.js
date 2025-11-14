import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [prompt, setPrompt] = useState('A medieval castle on a mountain with a village below');
  const [worldSize, setWorldSize] = useState(512);
  const [complexity, setComplexity] = useState('medium');
  const [includeTerrain, setIncludeTerrain] = useState(true);
  const [includeStructures, setIncludeStructures] = useState(true);
  const [includeObjects, setIncludeObjects] = useState(true);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState('');
  const [progress, setProgress] = useState(0);
  const [isGenerating, setIsGenerating] = useState(false);
  const [recentJobs, setRecentJobs] = useState([]);

  useEffect(() => {
    if (jobId) {
      const interval = setInterval(() => {
        checkStatus(jobId);
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [jobId]);

  useEffect(() => {
    fetchRecentJobs();
  }, []);

  const fetchRecentJobs = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/jobs?limit=5`);
      setRecentJobs(response.data.jobs || []);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setStatus('Please enter a world description');
      return;
    }

    setIsGenerating(true);
    setStatus('Starting generation...');
    setProgress(0);

    try {
      const response = await axios.post(`${API_URL}/api/generate`, {
        prompt,
        world_size: worldSize,
        complexity,
        include_terrain: includeTerrain,
        include_structures: includeStructures,
        include_objects: includeObjects
      });

      setJobId(response.data.job_id);
      setStatus('Generation queued...');
    } catch (error) {
      setStatus(`Error: ${error.response?.data?.detail || error.message}`);
      setIsGenerating(false);
    }
  };

  const checkStatus = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/api/status/${id}`);
      const data = response.data;

      setProgress(data.progress || 0);
      setStatus(`Status: ${data.status} (${data.progress || 0}%)`);

      if (data.status === 'completed') {
        setStatus('Generation completed! Download available below.');
        setIsGenerating(false);
        fetchRecentJobs();
      } else if (data.status === 'failed') {
        setStatus(`Generation failed: ${data.error || 'Unknown error'}`);
        setIsGenerating(false);
      }
    } catch (error) {
      setStatus(`Error checking status: ${error.message}`);
      setIsGenerating(false);
    }
  };

  const handleDownload = async (id) => {
    try {
      const response = await axios.get(`${API_URL}/api/download/${id}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `world_${id}.rbxlx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setStatus(`Error downloading: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>🎮 Roblox World Generator</h1>
          <p>Create amazing Roblox worlds from text descriptions using AI</p>
        </header>

        <div className="main-content">
          <div className="generator-panel">
            <div className="section">
              <label htmlFor="prompt">World Description</label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your world... (e.g., 'A medieval castle on a mountain with a village below')"
                rows={4}
                disabled={isGenerating}
              />
            </div>

            <div className="section">
              <label htmlFor="worldSize">World Size: {worldSize} studs</label>
              <input
                id="worldSize"
                type="range"
                min="128"
                max="2048"
                step="64"
                value={worldSize}
                onChange={(e) => setWorldSize(parseInt(e.target.value))}
                disabled={isGenerating}
              />
            </div>

            <div className="section">
              <label>Complexity</label>
              <div className="button-group">
                {['low', 'medium', 'high'].map((comp) => (
                  <button
                    key={comp}
                    className={`complexity-btn ${complexity === comp ? 'active' : ''}`}
                    onClick={() => setComplexity(comp)}
                    disabled={isGenerating}
                  >
                    {comp.charAt(0).toUpperCase() + comp.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <div className="section">
              <label>Include:</label>
              <div className="checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={includeTerrain}
                    onChange={(e) => setIncludeTerrain(e.target.checked)}
                    disabled={isGenerating}
                  />
                  Terrain
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={includeStructures}
                    onChange={(e) => setIncludeStructures(e.target.checked)}
                    disabled={isGenerating}
                  />
                  Structures
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={includeObjects}
                    onChange={(e) => setIncludeObjects(e.target.checked)}
                    disabled={isGenerating}
                  />
                  Objects
                </label>
              </div>
            </div>

            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={isGenerating}
            >
              {isGenerating ? 'Generating...' : 'Generate World'}
            </button>

            {isGenerating && (
              <div className="progress-section">
                <div className="progress-bar">
                  <div
                    className="progress-fill"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="progress-text">{progress}%</p>
              </div>
            )}

            {status && (
              <div className={`status ${isGenerating ? 'info' : ''}`}>
                {status}
              </div>
            )}

            {jobId && !isGenerating && status.includes('completed') && (
              <button
                className="download-btn"
                onClick={() => handleDownload(jobId)}
              >
                Download World File
              </button>
            )}
          </div>

          <div className="sidebar">
            <h2>Recent Generations</h2>
            {recentJobs.length === 0 ? (
              <p className="empty-state">No recent generations</p>
            ) : (
              <div className="job-list">
                {recentJobs.map((job) => (
                  <div key={job.job_id} className="job-item">
                    <div className="job-prompt">
                      {job.prompt || 'No description'}
                    </div>
                    <div className="job-status">
                      <span className={`status-badge ${job.status}`}>
                        {job.status}
                      </span>
                      <span className="job-progress">{job.progress}%</span>
                    </div>
                    {job.status === 'completed' && (
                      <button
                        className="download-small-btn"
                        onClick={() => handleDownload(job.job_id)}
                      >
                        Download
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;



