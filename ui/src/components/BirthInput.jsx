import React, { useState, useEffect } from 'react';

const BirthInput = ({ onSubmit, isLoading }) => {
    const [formData, setFormData] = useState({
        name: '',
        gender: 'male',
        dob: '1989-02-24',
        tob: '16:30:00',
        lat: '',
        lon: '',
        timezone: '',
        city: '',
        ayanamsa: 1
    });

    const [searchResults, setSearchResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [showDropdown, setShowDropdown] = useState(false);

    // Debounce search
    useEffect(() => {
        const timer = setTimeout(() => {
            if (formData.city && formData.city.length > 2 && showDropdown) {
                searchCities(formData.city);
            }
        }, 500);

        return () => clearTimeout(timer);
    }, [formData.city]);

    const searchCities = async (query) => {
        setIsSearching(true);
        try {
            const response = await fetch(`/api/v1/geo/search?q=${encodeURIComponent(query)}`);
            if (response.ok) {
                const data = await response.json();
                setSearchResults(data);
            }
        } catch (error) {
            console.error("Error searching cities:", error);
        } finally {
            setIsSearching(false);
        }
    };

    const handleCitySelect = (city) => {
        setFormData(prev => ({
            ...prev,
            city: city.name,
            lat: city.lat,
            lon: city.lon,
            timezone: city.timezone
        }));
        setShowDropdown(false);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        if (name === 'city') {
            setShowDropdown(true);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            ...formData,
            lat: parseFloat(formData.lat),
            lon: parseFloat(formData.lon),
            timezone: parseFloat(formData.timezone),
            ayanamsa: parseInt(formData.ayanamsa)
        });
    };

    return (
        <div className="card">
            <h2 style={{ marginTop: 0, marginBottom: '20px' }}>Birth Details</h2>
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <label>Name</label>
                    <input
                        type="text"
                        name="name"
                        className="input-field"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Enter Name"
                    />
                </div>

                <div className="input-group">
                    <label>Gender</label>
                    <select
                        name="gender"
                        className="input-field"
                        value={formData.gender}
                        onChange={handleChange}
                    >
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <div className="input-group">
                    <label>City / Place of Birth</label>
                    <div style={{ position: 'relative' }}>
                        <input
                            type="text"
                            name="city"
                            className="input-field"
                            value={formData.city}
                            onChange={handleChange}
                            placeholder="Start typing city name..."
                            required
                            autoComplete="off"
                        />
                        {isSearching && <div style={{ position: 'absolute', right: 10, top: 12, fontSize: '12px' }}>Loading...</div>}

                        {showDropdown && searchResults.length > 0 && (
                            <ul style={{
                                position: 'absolute',
                                top: '100%',
                                left: 0,
                                right: 0,
                                background: 'var(--card-bg)',
                                border: '1px solid var(--border-color)',
                                listStyle: 'none',
                                padding: 0,
                                margin: 0,
                                zIndex: 1000,
                                maxHeight: '200px',
                                overflowY: 'auto'
                            }}>
                                {searchResults.map((city, idx) => (
                                    <li
                                        key={idx}
                                        onClick={() => handleCitySelect(city)}
                                        style={{
                                            padding: '10px',
                                            cursor: 'pointer',
                                            borderBottom: '1px solid var(--border-color)',
                                            fontSize: '0.9rem'
                                        }}
                                        onMouseEnter={(e) => e.target.style.background = 'var(--input-bg)'}
                                        onMouseLeave={(e) => e.target.style.background = 'transparent'}
                                    >
                                        <div style={{ fontWeight: 'bold' }}>{city.name}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{city.country} ({city.timezone})</div>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>

                <div className="input-group">
                    <label>Date of Birth</label>
                    <input
                        type="date"
                        name="dob"
                        className="input-field"
                        value={formData.dob}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="input-group">
                    <label>Time of Birth</label>
                    <input
                        type="time"
                        name="tob"
                        step="1"
                        className="input-field"
                        value={formData.tob}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="grid-layout" style={{ gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                    <div className="input-group">
                        <label>Latitude</label>
                        <input
                            type="number"
                            name="lat"
                            step="0.0001"
                            className="input-field"
                            value={formData.lat}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="input-group">
                        <label>Longitude</label>
                        <input
                            type="number"
                            name="lon"
                            step="0.0001"
                            className="input-field"
                            value={formData.lon}
                            onChange={handleChange}
                            required
                        />
                    </div>
                </div>

                <div className="input-group">
                    <label>Timezone (Offset from UTC)</label>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '5px' }}>
                        Example: 5.5 for India, -5 for EST. Please verify.
                    </div>
                    <input
                        type="number"
                        name="timezone"
                        step="0.5"
                        className="input-field"
                        value={formData.timezone}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit" className="btn-primary" disabled={isLoading}>
                    {isLoading ? 'Calculating...' : 'Generate Kundli'}
                </button>
            </form>
        </div>
    );
};

export default BirthInput;
