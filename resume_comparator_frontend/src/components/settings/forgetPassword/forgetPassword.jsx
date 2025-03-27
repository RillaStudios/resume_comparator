import React, { useState } from 'react';
import { changePassword } from '../../service/authService';
import './ForgetPassword.css';
import { toast } from 'react-toastify';


/*
 Author: Michael Tamatey
 Date: 20250222
 Description: This class is for user change password
*/
const ForgetPassword = ({ onClose }) => {
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');

    const handleChangePassword = async () => {
        if (!oldPassword || !newPassword) {
            toast.error('Please enter both old and new passwords');
            return;
        }

        try {
            await changePassword(oldPassword, newPassword);
            toast.success('Password changed successfully')
            onClose(); // Close modal after success
        } catch (err) {
            alert('Error changing password');
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>Change Password</h3>
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
                    <button onClick={handleChangePassword} className="password-button">Confirm</button>
                    <button onClick={onClose} className="cancel-button">Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default ForgetPassword;
