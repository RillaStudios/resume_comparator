import React from "react";
import { Outlet } from "react-router-dom"; // Outlet for rendering pages
import "./DashboardLayout.css";
import SideNav from "./components/sideAndTop/sidebar/sideNav";
import TopNavBar from "./components/sideAndTop/topNavbar/topNavBar";
/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class controls the dashboard layout
*/
function DashboardLayout({ logout }) {
  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <SideNav logout={logout} />

      {/* Main Content Area */}
      <div className="main-content">
        {/* Profile Header at Top Right */}
        <TopNavBar />

        {/* Dynamic Page Content */}
        <div className="page-content">
          <Outlet /> {/* This renders the page based on route */}
        </div>
      </div>
    </div>
  );
}

export default DashboardLayout;