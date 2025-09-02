import React, { useState } from "react";
import "./App.css";
import { CloudUpload } from "lucide-react";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/api/detect/', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">Authentica</div>
        <div className="nav-links">
          <a href="#">About</a>
          <a href="#">Features</a>
          <a href="#">Contact</a>
        </div>
      </nav>

      {/* Main Section */}
      <main className="main">
        <h1 className="title">AuthenTica</h1>
        <h2 className="subtitle">Your Deepfake Detector</h2>

        <div className="upload-box">
          <CloudUpload className="upload-icon" size={64} />
          <p className="upload-text">Upload Image or Video</p>
          <input
            type="file"
            accept="image/*,video/*"
            onChange={handleFileUpload}
            style={{ display: 'none' }}
            id="file-upload"
          />
          <label htmlFor="file-upload" className="upload-btn">
            {loading ? 'Analyzing...' : 'Upload'}
          </label>
        </div>

        {/* Results */}
        {result && (
          <div className="results">
            <h3>Detection Results</h3>
            <div className="result-card">
              <p><strong>File:</strong> {result.file_name}</p>
              <p><strong>Status:</strong> 
                <span className={result.status === 'AUTHENTIC' ? 'authentic' : 'manipulated'}>
                  {result.status}
                </span>
              </p>
              <p><strong>Authenticity:</strong> {result.authenticity_percentage}%</p>
              <p><strong>Manipulation:</strong> {result.manipulation_percentage}%</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
