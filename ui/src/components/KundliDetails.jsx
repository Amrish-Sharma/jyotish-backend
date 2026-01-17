import React from 'react';

const KundliDetails = ({ basicDetails, ghatakDetails }) => {
    if (!basicDetails) return null;

    return (
        <div className="card" style={{ marginTop: '20px' }}>
            <h3>Advanced Details</h3>

            <div className="grid-layout" style={{ gridTemplateColumns: '1fr 1fr', gap: '20px' }}>

                {/* Avakahada / Basic Details */}
                <div>
                    <h4 style={{ color: 'var(--accent-color)' }}>Avakahada & Panchang</h4>
                    <table className="data-table">
                        <tbody>
                            <tr><td>Ascendant Lord</td><td>{basicDetails.ascendant_lord}</td></tr>
                            <tr><td>Rasi Lord</td><td>{basicDetails.rasi_lord}</td></tr>
                            <tr><td>Nakshatra Lord</td><td>{basicDetails.nakshatra_lord}</td></tr>
                            <tr><td>Nakshatra - Charan</td><td>{basicDetails.nakshatra_charan}</td></tr>
                            <tr><td>Yoga</td><td>{basicDetails.yoga}</td></tr>
                            <tr><td>Karan</td><td>{basicDetails.karan}</td></tr>
                            <tr><td>Tithi</td><td>{basicDetails.tithi}</td></tr>
                            <tr><td>Day</td><td>{basicDetails.day}</td></tr>
                            <tr><td>Gana</td><td>{basicDetails.gana}</td></tr>
                            <tr><td>Yoni</td><td>{basicDetails.yoni}</td></tr>
                            <tr><td>Nadi</td><td>{basicDetails.nadi}</td></tr>
                            <tr><td>Varan</td><td>{basicDetails.varan}</td></tr>
                            <tr><td>Vashya</td><td>{basicDetails.vashya}</td></tr>
                        </tbody>
                    </table>
                </div>

                {/* Ghatak Chakra */}
                <div>
                    <h4 style={{ color: '#ff6b6b' }}>Ghatak Chakra (Inauspicious)</h4>
                    {ghatakDetails ? (
                        <table className="data-table">
                            <tbody>
                                <tr><td>Month</td><td>{ghatakDetails.month}</td></tr>
                                <tr><td>Tithi</td><td>{ghatakDetails.tithi}</td></tr>
                                <tr><td>Day</td><td>{ghatakDetails.day}</td></tr>
                                <tr><td>Nakshatra</td><td>{ghatakDetails.nakshatra}</td></tr>
                                <tr><td>Yoga</td><td>{ghatakDetails.yoga}</td></tr>
                                <tr><td>Karan</td><td>{ghatakDetails.karan}</td></tr>
                                <tr><td>Prahar</td><td>{ghatakDetails.prahar}</td></tr>
                                <tr><td>Moon</td><td>{ghatakDetails.moon}</td></tr>
                            </tbody>
                        </table>
                    ) : (
                        <p>No Ghatak details available</p>
                    )}
                </div>

            </div>
        </div>
    );
};

export default KundliDetails;
