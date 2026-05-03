import React, { useState } from 'react';

function CreateCourse() {
  const [course, setCourse] = useState({
    name: '',
    details: '',
    video: '',
    pdf: '',
    price: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCourse(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Course Created Successfully!');
    // Backend e send korar logic ekhane ashbe pore
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(to right, #e0eafc, #cfdef3)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '30px'
    }}>
      <form onSubmit={handleSubmit} style={{
        width: '450px',
        backgroundColor: 'white',
        padding: '25px',
        borderRadius: '8px',
        boxShadow: '0 0 15px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ textAlign: 'center', marginBottom: '20px', color: '#007bff' }}>Create New Course</h2>

        <label>Course Name:</label>
        <input
          type="text"
          name="name"
          value={course.name}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        />

        <label>Course Details:</label>
        <textarea
          name="details"
          value={course.details}
          onChange={handleChange}
          rows="4"
          required
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        ></textarea>

        <label>Video Link:</label>
        <input
          type="text"
          name="video"
          value={course.video}
          onChange={handleChange}
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        />

        <label>Upload PDF:</label>
        <input
          type="file"
          accept="application/pdf"
          name="pdf"
          onChange={(e) => setCourse({ ...course, pdf: e.target.files[0] })}
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        />

        <label>Price:</label>
        <input
          type="number"
          name="price"
          value={course.price}
          onChange={handleChange}
          required
          style={{ width: '100%', padding: '8px', margin: '10px 0' }}
        />

        <button type="submit" style={{
          width: '100%',
          padding: '10px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '10px'
        }}>Submit</button>
      </form>
    </div>
  );
}

export default CreateCourse;
