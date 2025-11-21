import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

import Login from './pages/login';
import Dashboard from './pages/dashboard';

function App() {
    return (
        <BrowserRouter>
            {/* Barre de navigation */}
            <nav style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
                {/* Link agit comme un bouton pour changer d'URL */}
                <Link to="/" style={{ marginRight: '10px' }}>Dashboard</Link>
                <Link to="/login">Login</Link>
            </nav>

            <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/login" element={<Login />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;