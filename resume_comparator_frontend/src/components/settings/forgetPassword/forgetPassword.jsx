import React, { useState, useContext } from 'react';
import { useAuth } from '../../service/authContext'; // Use the AuthContext hook
import './ForgetPassword.css';
import { toast } from 'react-toastify';
import spinner from "../../../assets/image/loadingSpinner.gif";

/*
 Author: Michael Tamatey/
 Date: 20250222
 Description: This class is for user password change with validation
*/

const ForgetPassword = ({ onClose }) => {
    const { user, changePassword: changePasswordService } = useAuth();
    const [username, setUsername] = useState('');
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChangePassword = async () => {
        
        if (!username || !oldPassword || !newPassword) {
            toast.error('Please fill in all fields');
            return;
        }

        if (username !== user?.username) {
            toast.error('Entered username does not match the logged-in user');
            return;
        }
        
        if (oldPassword === newPassword) {
            toast.error('New password cannot be the same as the old password');
            return;
        }
    
        try {
            setLoading(true); 
            await changePasswordService(username, oldPassword, newPassword);
            onClose(); 
        } catch (err) {
            toast.error('Error changing password. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>Change Password</h3>
                <input 
                    type="text" 
                    placeholder="Username" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)} 
                    className="password-input"
                />
                <input 
                    type="password" 
                    placeholder="Old Password" 
                    value={oldPassword} 
                    onChange={(e) => setOldPassword(e.target.value)} 
                    className="password-input"
                />
                <input 
                    type="password" 
                    placeholder="New Password" 
                    value={newPassword} 
                    onChange={(e) => setNewPassword(e.target.value)} 
                    className="password-input"
                />
                <div className="modal-buttons">
                    <button onClick={handleChangePassword} className="password-button">
                        Confirm
                    </button>
                    <button onClick={onClose} className="cancel-button">
                        Cancel
                    </button>
                </div>
            </div>
            {loading && (
                    <div className="loading-spin">
                        <div className="loading-spinner">
                            <img src={spinner} alt="Loading..." />
                        </div>
                    </div>
                )}
        </div>
    );
};

export default ForgetPassword;