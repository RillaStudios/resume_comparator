import React from "react"; // Import React
import "./topNavBar.css"; // Import CSS for styling
/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class controls the top navigation bar
*/
const Navbar = () => {
  //const firstName = localStorage.getItem("firstName") || "";
  //const lastName = localStorage.getItem("lastName") || "";
  //const role = localStorage.getItem("role") || "";

  // Hard-coded name and role
  const firstName = "CIS";
  const lastName = "OJT";
  const role = "DIRECTOR";

  return (
    <nav className="navbar">
      
        {/* Profile Section */}
        <div className="profile-section">
          <div className="profile-info">
            <strong>{`${firstName} ${lastName}`}</strong>
            <div className="profile-role">{role}</div>
          </div>
        </div>
      
    </nav>
  );
};

export default Navbar;