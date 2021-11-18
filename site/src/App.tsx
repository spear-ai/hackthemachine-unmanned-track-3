import React from 'react';
import GithubCorner from 'react-github-corner';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://www.hackthemachine.ai/track3"
          target="_blank"
          rel="noopener noreferrer"
        >
          Our mission
        </a>
      </header>
      <GithubCorner
        bannerColor="#d92f20"
        href="https://github.com/spear-ai/hackthemachine-unmanned-track-3"
        octoColor="#2b2b2b"
      />
    </div>
  );
}

export default App;
