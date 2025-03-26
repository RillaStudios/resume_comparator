/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class contains sidebar data
*/
const role = localStorage.getItem("role"); // Get user role

// Define all sidebar items
const allSideBarData = [
  {
    title: "Home",
    path: "/",
    cName: "nav-text",
  },
  {
    title: "Reports",
    path: "/reports",
    cName: "nav-text",
  },
  {
    title: "Account",
    path: "/account", 
    cName: "nav-text",
  },
  // Uncomment if needed
  // {
  //   title: "Settings",
  //   path: "/settings",
  //   icon: <CiSettings />,
  //   cName: "nav-text",
  // },
];

// Filter based on role
const SideBarData = allSideBarData.filter((item) => {
  if (role === "DIRECTOR") {
    return item.title !== "Reports"; // Hide Reports for DIRECTOR
  }
  return true; // RECRUITER sees everything
});

export default SideBarData;