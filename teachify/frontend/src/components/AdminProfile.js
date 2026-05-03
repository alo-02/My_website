import React from 'react';

function AdminProfile() {
  const handleView = () => {
    alert('View button clicked!');
  };

  const handleDelete = () => {
    alert('Delete button clicked!');
  };

  const handleEdit = () => {
    alert('Edit button clicked!');
  };

  return (
    <div style={styles.page}>
      <div style={styles.content}>
        <h2 style={styles.heading}>Admin Profile</h2>

        <div style={styles.buttonGroup}>
          <button style={styles.button} onClick={handleView}>View</button>
          <button style={styles.button} onClick={handleDelete}>Delete</button>
          <button style={styles.button} onClick={handleEdit}>Edit</button>
        </div>
      </div>

      <footer style={styles.footer}>
        © 2025 Teachify | Admin Dashboard
      </footer>
    </div>
  );
}

const styles = {
  page: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    background: 'linear-gradient(to bottom right, #e3d7f3, #e8d6f8)',
  },
  content: {
    flex: 1,
    textAlign: 'center',
    paddingTop: '80px',
  },
  heading: {
    fontSize: '28px',
    color: '#333',
    marginBottom: '40px',
  },
  buttonGroup: {
    display: 'flex',
    justifyContent: 'center',
    gap: '30px',
    marginTop: '-10px', // Moves buttons upward
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#7f5af0',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
  },
  footer: {
    backgroundColor: '#102542', // matching navbar
    color: 'white',
    textAlign: 'center',
    padding: '12px 0',
    fontSize: '14px',
    marginTop: 'auto',
  },
};

export default AdminProfile;



//http://localhost:3000/admin/profile