import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function TeacherProfile() {
  const [teacher, setTeacher] = useState({
    name: 'Mr. John Doe',
    id: 'T12345',
    contact: '0123456789',
    address: 'Dhaka, Bangladesh',
    course: 'Web Development',
    courses: ['Web Development', 'Data Structures']
  });

  const [editing, setEditing] = useState(false);
  const navigate = useNavigate();

  const handleDeleteCourse = (index) => {
    const updatedCourses = [...teacher.courses];
    updatedCourses.splice(index, 1);
    setTeacher({ ...teacher, courses: updatedCourses });
  };

  const handleInputChange = (e) => {
    setTeacher({ ...teacher, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    setEditing(false);
    alert('Profile updated!');
  };

  return (
    <div style={{ 
      minHeight: '100vh',
      background: 'linear-gradient(to right, #d3cce3, #e9e4f0)',
      display: 'flex',
      flexDirection: 'column'
    }}>
      <div style={{
        flex: '1',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <div style={{
          width: '400px',
          padding: '25px',
          borderRadius: '8px',
          backgroundColor: 'white',
          boxShadow: '0 0 15px rgba(0,0,0,0.1)',
          textAlign: 'left'
        }}>
          <h2 style={{ color: 'purple', marginBottom: '10px' }}>📚 Teacher Profile
            {!editing && (
              <button
                onClick={() => setEditing(true)}
                style={{
                  float: 'right',
                  backgroundColor: '#007bff',
                  color: 'white',
                  border: 'none',
                  padding: '5px 10px',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >Edit Profile</button>
            )}
          </h2>

          {!editing ? (
            <>
              <p><strong>Name:</strong> {teacher.name} &nbsp;&nbsp; <strong>ID:</strong> {teacher.id}</p>
              <h3 style={{ marginTop: '20px' }}>📖 My Courses:</h3>
              {teacher.courses.map((course, index) => (
                <div key={index} style={{ marginBottom: '10px' }}>
                  {course}
                  <button
                    onClick={() => handleDeleteCourse(index)}
                    style={{
                      backgroundColor: 'red',
                      color: 'white',
                      border: 'none',
                      marginLeft: '10px',
                      padding: '3px 10px',
                      borderRadius: '5px',
                      cursor: 'pointer'
                    }}
                  >Delete</button>
                </div>
              ))}

              <div style={{ marginTop: '20px' }}>
                <button
                  onClick={() => navigate('/create-course')}
                  style={{
                    backgroundColor: 'green',
                    color: 'white',
                    border: 'none',
                    padding: '7px 15px',
                    borderRadius: '5px',
                    cursor: 'pointer'
                  }}
                >Create Course</button>
              </div>
            </>
          ) : (
            <>
              <div style={{ marginBottom: '10px' }}>
                <label><strong>Name:</strong></label><br />
                <input
                  type="text"
                  name="name"
                  value={teacher.name}
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '5px', marginTop: '5px' }}
                />
              </div>
              <div style={{ marginBottom: '10px' }}>
                <label><strong>Contact:</strong></label><br />
                <input
                  type="text"
                  name="contact"
                  value={teacher.contact}
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '5px', marginTop: '5px' }}
                />
              </div>
              <div style={{ marginBottom: '10px' }}>
                <label><strong>Address:</strong></label><br />
                <input
                  type="text"
                  name="address"
                  value={teacher.address}
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '5px', marginTop: '5px' }}
                />
              </div>
              <div style={{ marginBottom: '10px' }}>
                <label><strong>Course:</strong></label><br />
                <input
                  type="text"
                  name="course"
                  value={teacher.course}
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '5px', marginTop: '5px' }}
                />
              </div>
              <button
                onClick={handleSave}
                style={{
                  backgroundColor: '#28a745',
                  color: 'white',
                  border: 'none',
                  padding: '7px 15px',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >Save</button>
            </>
          )}
        </div>
      </div>

      <footer style={{
        backgroundColor: '#001f3f',
        color: 'white',
        textAlign: 'center',
        padding: '12px'
      }}>
        © 2025 Teachify. Empowering Educators & Learners.
      </footer>
    </div>
  );
}

export default TeacherProfile;




//http://localhost:3000/teacher/profile