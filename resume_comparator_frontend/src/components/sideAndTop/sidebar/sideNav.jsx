import React from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom"; // ✅ Import useNavigate
import SideBarData from "./sideBarData"; // ✅ Import SideBarData
import cvLogo from "../../../assets/image/logo.png"; // ✅ Import logo
import "./sideNav.css";
import { IconContext } from "react-icons";
import { FaSignOutAlt } from "react-icons/fa";

/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class controls the sidebar navigation
*/
const SideNav = (props) => {
  const location = useLocation(); // ✅ Get current path
  const navigate = useNavigate(); // ✅ For redirecting after logout

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    // Redirect to the login page
    navigate("/login");
  };

  return (
    <IconContext.Provider value={{ color: "" }}>
      <div className="side-nav">
        {/* Logo */}
        <div className="logo-container">
          <img src={cvLogo} alt="Logo" className="logo" />
        </div>

        {/* Navigation Menu */}
        <nav className="nav-menu">
          <ul className="nav-menu-items">
            {SideBarData.map((item, index) => (
              <li
                key={index}
                className={`nav-text ${location.pathname === item.path ? "active" : ""}`}
              >
                <NavLink
                  to={item.path}
                  className={({ isActive }) => (isActive ? "active-link" : "")}
                >
                  {item.icon}
                  <span>{item.title}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* Logout Button at the Bottom */}
        <div className="logout-container">
          <button onClick={logout} className="logout-btn">
            <span>Logout</span>
            <FaSignOutAlt className="logout-icon" />
          </button>
        </div>
      </div>
    </IconContext.Provider>
  );
};

export default SideNav;