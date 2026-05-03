import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/signup');
  };

  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const images = ['/slide1.jpg', '/slide2.jpg', '/slide3.jpg'];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{
      display: 'flex',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #e0f7ff, #c4dbf6)',
      padding: '0',
      boxSizing: 'border-box'
    }}>
      
      {/* Left Section */}
      <div style={{
        flex: 1,
        padding: '60px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center'
      }}>
        <h1 style={{ fontSize: '48px', fontWeight: 'bold', color: '#1f2e4d' }}>Learn Anytime, Anywhere</h1>
        <p style={{ marginTop: '20px', maxWidth: '550px', fontSize: '20px', color: '#333' }}>
          Teachify offers high-quality courses taught by expert teachers. Start your learning journey now!
        </p>
        <button
          onClick={handleGetStarted}
          style={{
            marginTop: '30px',
            padding: '12px 28px',
            backgroundColor: '#1f2e4d',
            color: '#fff',
            border: 'none',
            borderRadius: '6px',
            fontSize: '16px',
            cursor: 'pointer'
          }}
        >
          Get Started
        </button>
      </div>

      {/* Right Section - Slideshow */}
      <div style={{
        flex: 1,
        position: 'relative',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        overflow: 'hidden'
      }}>
        {images.map((image, index) => (
          <img
            key={index}
            src={image}
            alt={`Slide ${index + 1}`}
            style={{
              position: 'absolute',
              width: '90%',
              height: '80%',
              objectFit: 'cover',
              borderRadius: '15px',
              opacity: currentImageIndex === index ? 1 : 0,
              transition: 'opacity 1s ease-in-out',
              boxShadow: currentImageIndex === index ? '0 10px 25px rgba(0, 0, 0, 0.3)' : 'none'
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default Home;
