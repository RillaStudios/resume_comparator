import React from "react";
import { Link } from "react-router-dom";
import "./navbar.modules.css";
import { useState } from 'react';
import logo from '../../assets/image/logo.png';
import closeNav from "../../assets/image/closeIcon.png";
import menuIcon from "../../assets/image/menuIcon.jpg";

/*
 Author: Michael Tamatey
 Date: 20250222
 Description: Navbar
*/

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // async function handleLogout() {
  //   try {
  //     await auth.signOut();
  //     window.location.href = "/signin"
  //   } catch (e) {
  //     console.e("Error logging out:")
  //   }
  // }

  return (
    <nav className="navbar">
      <div className="navbar-container">

        <Link to="/">
        <img src={logo} className="App-logo" alt="logo" />
        </Link>
        <img
          className="menu-btn"
          src={isMenuOpen ? closeNav : menuIcon}
          alt="menu-button"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        />
        <ul className="nav-menu">

          <li className="nav-item">
            <Link to="/" className="nav-link">Home</Link>
          </li>
          <li className="nav-item">
            <Link to="/reports" className="nav-link">Reports</Link>
          </li>
          <li className="nav-item">
            <Link to="/account" className="nav-link">Account</Link>
          </li>
          {/* <li className="nav-item">
            <Link to="/signin" className="nav-link" onClick={handleLogout}>Log out</Link>
          </li> */}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;