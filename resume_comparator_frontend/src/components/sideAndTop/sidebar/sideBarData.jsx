/*
 Author: Michael Tamatey/ Navjot Kaur
 Date: 20250222
 Description: This class contains sidebar data
*/
const role = "DIRECTOR"; // Get user role

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
];

// Filter based on role
const SideBarData = allSideBarData.filter((item) => {
  if (role === "DIRECTOR") {
    return item.title !== "";
  }
  return true; 
});

export default SideBarData;