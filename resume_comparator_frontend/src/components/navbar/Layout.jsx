import React from 'react'
import { Outlet } from "react-router-dom";
import Navbar from "./navbar";

const layout = () => {
  return (
    <>
      <Navbar />
      <Outlet /> {/* This will render the current page's content */}
    </>
  )
}

export default layout
