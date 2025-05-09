import React, { useState, useEffect } from "react"; 
import "./topNavBar.css"; 
import { getProfile } from "../../service/authService";
import ProfilePic from '../../../assets/image/profilePic.png';
import { Link } from 'react-router-dom';

/*
 Author: Michael Tamatey / Navjot Kaur
 Date: 20250222
 Description: This class controls the top navigation bar
*/

const Navbar = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await getProfile();
        setUser(response.data);
      } catch (err) {
        console.error("Failed to fetch profile");
      }
    };
    fetchUser();
  }, []);

  return (
    <nav className="navbar">
      {/* Profile Section */}
      <div className="profile-section">
        <div className="profile-info">
          <div className="hero-image-navbar">
          <Link to="/account">
          <img src={ProfilePic} alt="Profile" />
          </Link>
          </div>
          {user ? (
            <>
              <strong>{`${user.first_name} ${user.last_name}`} | </strong>
              <div className="profile-role">{user.role}</div>
            </>
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;