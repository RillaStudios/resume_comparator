import React, { useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import SideBarData from "./sideBarData";
import cvLogo from "../../../assets/image/logo.png";
import "./sideNav.css";
import { IconContext } from "react-icons";
import { FaSignOutAlt } from "react-icons/fa";
import { toast } from "react-toastify";
import spinner from "../../../assets/image/loadingSpinner.gif"; 

/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class controls the sidebar navigation
*/
const SideNav = (props) => {
  const [loading, setLoading] = useState(false); // Loading state for logout
  const location = useLocation();
  const navigate = useNavigate();

  const logout = () => {
    setLoading(true); // Set loading to true before starting logout
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    // Simulate async process (e.g., API call or other tasks)
    setTimeout(() => {
      setLoading(false); 
      navigate("/login"); 
      toast.success("You have been logged out.");
    }, 1000); 
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
            
              <>
                <span>Logout</span>
                <FaSignOutAlt className="logout-icon" />
              </>
            
          </button>
        </div>
        {loading && (
                <div className="loading-spin1">
                  <div className="loading-spinner1">
                    <img src={spinner} alt="Loading..." />
                  </div>
                </div>
              )}
      </div>
    </IconContext.Provider>
  );
};

export default SideNav;