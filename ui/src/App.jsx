import React, { useState } from 'react';
import './App.css';
import BirthInput from './components/BirthInput';
import KundliChart from './components/KundliChart';
import PlanetTable from './components/PlanetTable';
import DashaDisplay from './components/DashaDisplay';

function App() {
  const [kundliData, setKundliData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchKundli = async (formData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/v1/kundli/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to generate Kundli');
      }

      const data = await response.json();
      setKundliData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1 className="main-title">Jyotish Graph</h1>
        <p style={{ color: 'var(--text-secondary)' }}>Vedic Astrology Engine</p>
      </header>

      <div className="grid-layout">
        <div className="sidebar">
          <BirthInput onSubmit={fetchKundli} isLoading={loading} />
          {error && <div className="card error-msg">{error}</div>}
        </div>

        <div className="main-content">
          {kundliData ? (
            <>
              <div style={{ marginBottom: '20px' }}>
                <KundliChart
                  houses={kundliData.houses}
                  planets={kundliData.planets}
                  lagnaSign={kundliData.lagna_sign}
                />
              </div>

              <div className="grid-layout" style={{ gridTemplateColumns: '1fr 1fr' }}>
                <PlanetTable planets={kundliData.planets} />
                <DashaDisplay dasha={kundliData.dasha} />
              </div>
            </>
          ) : (
            <div className="card" style={{ textAlign: 'center', padding: '50px' }}>
              <h3 style={{ color: 'var(--text-secondary)' }}>Enter birth details to generate Kundli</h3>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
