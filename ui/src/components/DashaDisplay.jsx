import React, { useState } from 'react';

const DashaDisplay = ({ dasha }) => {
    const [expandedMd, setExpandedMd] = useState(null);

    if (!dasha || !dasha.mahadashas) return null;

    const toggleMd = (idx) => {
        setExpandedMd(expandedMd === idx ? null : idx);
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return '';
        return new Date(dateStr).toLocaleDateString();
    };

    return (
        <div className="card">
            <h3>Vimshottari Dasha</h3>
            <div className="dasha-list">
                {dasha.mahadashas.map((md, idx) => (
                    <div key={idx} style={{ marginBottom: '10px' }}>
                        <div
                            onClick={() => toggleMd(idx)}
                            style={{
                                background: 'var(--input-bg)',
                                padding: '10px',
                                borderRadius: '6px',
                                cursor: 'pointer',
                                display: 'flex',
                                justifyContent: 'space-between',
                                border: '1px solid var(--border-color)'
                            }}
                        >
                            <span style={{ fontWeight: 'bold', color: 'var(--accent-color)' }}>{md.planet}</span>
                            <span>{formatDate(md.start_date)} - {formatDate(md.end_date)}</span>
                        </div>

                        {expandedMd === idx && md.sub_periods && (
                            <div style={{ padding: '10px', paddingLeft: '20px', background: 'rgba(0,0,0,0.2)' }}>
                                {md.sub_periods.map((ad, adIdx) => (
                                    <div key={adIdx} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '5px' }}>
                                        <span>{md.planet} - {ad.planet}</span>
                                        <span style={{ color: 'var(--text-secondary)' }}>{formatDate(ad.end_date)}</span>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default DashaDisplay;
