import React from 'react';

const PlanetTable = ({ planets }) => {
    return (
        <div className="card">
            <h3>Planetary Positions</h3>
            <table className="data-table">
                <thead>
                    <tr>
                        <th>Planet</th>
                        <th>Sign</th>
                        <th>Direct/Retro</th>
                        <th>Degree</th>
                    </tr>
                </thead>
                <tbody>
                    {planets.map(p => (
                        <tr key={p.id}>
                            <td>{p.name}</td>
                            <td>{p.sign}</td>
                            <td>{p.is_retrograde ? <span style={{ color: '#ff6b6b' }}>R</span> : 'D'}</td>
                            <td>{p.longitude.toFixed(2)}°</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PlanetTable;
