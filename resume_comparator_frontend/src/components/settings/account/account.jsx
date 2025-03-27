import { useEffect, useState } from 'react';
import { getProfile, deleteAccount, logout } from '../../service/authService';
import { toast } from 'react-toastify';
import ProfilePic from '../../../assets/image/profilePic.png';
import ForgetPassword from '../forgetPassword/forgetPassword'; 
import './Account.css'; 


/*
 Author: Michael Tamatey
 Date: 20250222
 Description: This class is for user account
*/
const Account = () => {
    const [user, setUser] = useState(null);
    const [deletePassword, setDeletePassword] = useState('');
    const [showChangePassword, setShowChangePassword] = useState(false); // State for the popup

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await getProfile();
                setUser(response.data);
            } catch (err) {
                console.error('Failed to fetch profile');
            }
        };
        fetchUser();
    }, []);

    const handleDeleteAccount = async () => {
        try {
            await deleteAccount(deletePassword);
            toast.success('Account deleted successfully');
            logout();
            window.location.href = '/login';
        } catch (err) {
            toast.error('Error deleting account');
        }
    };

    return (
        <div className="account-container">
            {/* Hero Image */}
            <div className="hero-image">
                <img src={ProfilePic} alt="Profile" />
            </div>

            {/* Account Details Section */}
            <h2>Account Details</h2>
            {user ? (
                <>
                    <div className="account-details">
                        <div className="account-box"><p><strong>Username:</strong> {user.username}</p></div>
                        <div className="account-box"><p><strong>First Name:</strong> {user.first_name}</p></div>
                        <div className="account-box"><p><strong>Last Name:</strong> {user.last_name}</p></div>
                        <div className="account-box"><p><strong>Email:</strong> {user.email}</p></div>
                        <div className="account-box"><p><strong>Address:</strong> {user.address}</p></div>
                        <div className="account-box"><p><strong>Role:</strong> {user.role}</p></div>
                    </div>

                    {/* Delete Account Section */}
                    <div className="delete-section">
                        <h3>Delete Account</h3>
                        <p>This action cannot be undone.</p>
                        <input 
                            type="password" 
                            className="account-input"
                            placeholder="Confirm Password" 
                            onChange={(e) => setDeletePassword(e.target.value)} 
                        />
                        <button onClick={handleDeleteAccount} className="account-button">
                            Delete Account
                        </button>

                        {/* Change Password Link - Opens the Popup */}
                        <a href="#" className="change-password" onClick={() => setShowChangePassword(true)}>Change Password Here</a>
                    </div>
                </>
            ) : (
                <p className="loading-text">Loading...</p>
            )}

            {/* Render Change Password Popup when showChangePassword is true */}
            {showChangePassword && <ForgetPassword onClose={() => setShowChangePassword(false)} />}
        </div>
    );
};

export default Account;