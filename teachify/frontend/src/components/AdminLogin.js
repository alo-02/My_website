import React from "react";
import { useNavigate } from "react-router-dom";

function AdminLogin() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault(); // prevent page reload
    // Bypass login validation, directly navigate
    navigate("/admin/profile");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Admin</h2>
      <form onSubmit={handleLogin}>
        <input type="text" placeholder="Admin ID" style={inputStyle} /><br /><br />
        <input type="password" placeholder="Password" style={inputStyle} /><br /><br />
        <button type="submit" style={buttonStyle}>Login</button>
      </form>
    </div>
  );
}

const inputStyle = {
  width: "200px",
  padding: "8px",
  borderRadius: "5px",
  border: "1px solid gray"
};

const buttonStyle = {
  padding: "8px 16px",
  backgroundColor: "orange",
  color: "black",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer"
};

export default AdminLogin;

//http://localhost:3000/admin