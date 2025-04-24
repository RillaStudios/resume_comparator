import React from "react";
import { Link } from "react-router-dom";

/*
 Author: Michael Tamatey
 Date: 20250222
 Description: This component is used to display a 404 page when the user tries to access a page that does not exist.
 It is a simple page that informs the user that the page they are looking for does not exist and provides a link to go back to the home page.
*/
const NotFound = () => {
  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h1>404 - Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <Link to="/">Go Back Home</Link>
    </div>
  );
};

export default NotFound;