import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Contact from './components/Contact';
import About from './components/About';
import Login from './components/Login';
import Signup from './components/Signup';
import TeacherProfile from './components/TeacherProfile';
import CreateCourse from './components/CreateCourse';
import StudentProfile from './components/StudentProfile';
import AdminLogin from './components/AdminLogin';
import AdminProfile from './components/AdminProfile';

import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/about" element={<About />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/teacher/profile" element={<TeacherProfile />} />
        <Route path="/create-course" element={<CreateCourse />} />
        <Route path="/student/profile" element={<StudentProfile />} />
        <Route path="/admin" element={<AdminLogin />} />
        <Route path="/admin/profile" element={<AdminProfile />} />
      </Routes>
    </Router>
  );
}

export default App;
