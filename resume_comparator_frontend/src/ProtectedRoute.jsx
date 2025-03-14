import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./components/service/useAuth";

const ProtectedRoute = () => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated === undefined) return <div>Loading...</div>;

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;