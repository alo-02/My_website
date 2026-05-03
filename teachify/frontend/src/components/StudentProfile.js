import React, { useState } from 'react';

function StudentProfile() {
  const [isEditing, setIsEditing] = useState(false);
  const [studentInfo, setStudentInfo] = useState({
    name: 'Jane Smith',
    id: 'S56789',
    contact: '0123456789',
    address: 'Dhaka, Bangladesh'
  });

  const [search, setSearch] = useState('');
  const [courses] = useState([
    { name: 'Web Development' },
    { name: 'Machine Learning' },
    { name: 'Data Structures' }
  ]);

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleChange = (e) => {
    setStudentInfo({ ...studentInfo, [e.target.name]: e.target.value });
  };

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
  };

  const filteredCourses = courses.filter(course =>
    course.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{
      padding: '30px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      background: 'linear-gradient(to bottom right, #d6d6f5, #e6e6fa)',
      minHeight: '100vh'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '10px',
        boxShadow: '0px 0px 10px rgba(0,0,0,0.1)',
        padding: '30px',
        maxWidth: '700px',
        width: '100%'
      }}>
        <h2 style={{ color: '#6a1b9a', marginBottom: '10px' }}>🎓 Student Profile</h2>

        <div style={{ marginBottom: '15px' }}>
          <strong>Name:</strong> {isEditing ? (
            <input name="name" value={studentInfo.name} onChange={handleChange} />
          ) : studentInfo.name}
          <button onClick={handleEditToggle} style={{ marginLeft: '10px' }}>Edit Profile</button>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <strong>ID:</strong> {studentInfo.id}
        </div>

        <div style={{ marginBottom: '15px' }}>
          <strong>Contact:</strong> {isEditing ? (
            <input name="contact" value={studentInfo.contact} onChange={handleChange} />
          ) : studentInfo.contact}
        </div>

        <div style={{ marginBottom: '15px' }}>
          <strong>Address:</strong> {isEditing ? (
            <input name="address" value={studentInfo.address} onChange={handleChange} />
          ) : studentInfo.address}
        </div>

        <input
          type="text"
          placeholder="Search for a course..."
          value={search}
          onChange={handleSearchChange}
          style={{
            padding: '8px',
            width: '100%',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '5px'
          }}
        />

        <div>
          <h3>📚 Available Courses:</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {filteredCourses.map((course, index) => (
              <li key={index} style={{
                marginBottom: '10px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span>{course.name}</span>
                <button
                  style={{
                    backgroundColor: 'green',
                    color: 'white',
                    border: 'none',
                    padding: '5px 10px',
                    borderRadius: '5px',
                    cursor: 'pointer'
                  }}
                  onClick={() => alert(`Viewing and buying ${course.name}`)}
                >
                  View & Buy
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default StudentProfile;
