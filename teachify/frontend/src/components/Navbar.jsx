import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img src="/logo.png" alt="Logo" className="navbar-logo" />
        <span className="navbar-brand">Teachify</span>
      </div>
      <div className="navbar-center">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/contact" className="nav-link">Contact</Link>
        <Link to="/about" className="nav-link">About Us</Link>
      </div>
      <div className="navbar-right">
        <Link to="/login" className="nav-button login">Login</Link>
        <Link to="/signup" className="nav-button signup">Sign Up</Link>
      </div>
    </nav>
  );
}

export default Navbar;
