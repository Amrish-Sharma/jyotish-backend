import React from 'react';

// Simplified North Indian Chart (Diamond Style)
const KundliChart = ({ houses, planets, lagnaSign }) => {
    // Mapping of planets to houses
    // We need to group planets by house number
    const planetsByHouse = {};
    if (planets) {
        planets.forEach(p => {
            if (!planetsByHouse[p.house]) planetsByHouse[p.house] = [];
            planetsByHouse[p.house].push(p.name.substring(0, 2)); // Use first 2 chars
        });
    }

    // Determine Sign for each house
    // House 1 Sign = lagnaSign
    const getSign = (houseNum) => {
        if (!houses) return houseNum; // Fallback
        const house = houses.find(h => h.number === houseNum);
        return house ? house.sign : 0;
    }

    // SVG Coordinates for Diamond Chart
    // Represents 12 houses segments

    const width = 400;
    const height = 400;

    // Centers for text in each house (approximate)
    const pos = {
        1: { x: 200, y: 80 },
        2: { x: 100, y: 30 },
        3: { x: 30, y: 100 },
        4: { x: 80, y: 200 },
        5: { x: 30, y: 300 },
        6: { x: 100, y: 370 },
        7: { x: 200, y: 320 },
        8: { x: 300, y: 370 },
        9: { x: 370, y: 300 },
        10: { x: 320, y: 200 },
        11: { x: 370, y: 100 },
        12: { x: 300, y: 30 }
    };

    // Sign number positions (corners of houses usually)
    const signPos = {
        1: { x: 200, y: 120 },
        2: { x: 60, y: 20 },
        3: { x: 20, y: 60 },
        4: { x: 140, y: 200 },
        5: { x: 20, y: 340 },
        6: { x: 60, y: 380 },
        7: { x: 200, y: 280 },
        8: { x: 340, y: 380 },
        9: { x: 380, y: 340 },
        10: { x: 260, y: 200 },
        11: { x: 380, y: 60 },
        12: { x: 340, y: 20 }
    };

    return (
        <div className="card kundli-chart-container">
            <svg viewBox="0 0 400 400" className="kundli-svg">
                {/* Outer Frame */}
                <rect x="2" y="2" width="396" height="396" className="chart-line" />

                {/* Diagonals */}
                <line x1="0" y1="0" x2="400" y2="400" className="chart-line" />
                <line x1="400" y1="0" x2="0" y2="400" className="chart-line" />

                {/* Inner Diamond */}
                <line x1="200" y1="0" x2="0" y2="200" className="chart-line" />
                <line x1="0" y1="200" x2="200" y2="400" className="chart-line" />
                <line x1="200" y1="400" x2="400" y2="200" className="chart-line" />
                <line x1="400" y1="200" x2="200" y2="0" className="chart-line" />

                {/* Labels */}
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(num => (
                    <g key={num}>
                        {/* Sign Number */}
                        <text x={signPos[num].x} y={signPos[num].y} className="rash-num" textAnchor="middle">
                            {getSign(num)}
                        </text>

                        {/* Planets */}
                        <text x={pos[num].x} y={pos[num].y} className="planet-text" textAnchor="middle">
                            {planetsByHouse[num] ? planetsByHouse[num].join(' ') : ''}
                        </text>
                    </g>
                ))}
            </svg>
            <div style={{ textAlign: 'center', marginTop: '10px', color: 'var(--text-secondary)' }}>
                North Indian Chart
            </div>
        </div>
    );
};

export default KundliChart;
