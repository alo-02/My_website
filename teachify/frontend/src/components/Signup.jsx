import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Signup.css';

const Signup = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const initialRole = location.state?.role || 'student';
  const [role, setRole] = useState(initialRole);
  const [formData, setFormData] = useState({
    name: '', email: '', dob: '', contact: '',
    address: '', institution: '', password: '', confirmPassword: ''
  });

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Data to submit: ", { ...formData, role });
    navigate('/login');
  };

  return (
    <div className="signup-container">
      <h1>Teachify</h1>
      <h3>Sign up as:</h3>
      <div className="role-selector">
        <button className={role === 'student' ? 'active' : ''} onClick={() => setRole('student')}>Student</button>
        <button className={role === 'teacher' ? 'active' : ''} onClick={() => setRole('teacher')}>Teacher</button>
      </div>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Full Name" required onChange={handleChange} />
        <input name="email" placeholder="Email" type="email" required onChange={handleChange} />
        <input name="dob" placeholder="Date of Birth" type="date" required onChange={handleChange} />
        <input name="contact" placeholder="Contact" required onChange={handleChange} />
        <input name="address" placeholder="Address" required onChange={handleChange} />
        <input name="institution" placeholder="Institution Name" required onChange={handleChange} />
        <input name="password" placeholder="Create Password" type="password" required onChange={handleChange} />
        <input name="confirmPassword" placeholder="Confirm Password" type="password" required onChange={handleChange} />
        <button type="submit">Sign Up</button>
      </form>
      <p>Already signed up? <span onClick={() => navigate('/login')} className="form-link">Log In</span></p>
    </div>
  );
};

export default Signup;
