import { useEffect, useState } from 'react';
import { getProfile, deleteAccount, logout } from '../../service/authService';
import './Account.css'; // Import the CSS file
import { toast } from 'react-toastify';

const Account = () => {
    const [user, setUser] = useState(null);
    const [deletePassword, setDeletePassword] = useState('');

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
            toast.error('Error deleting account')
        }
    };

    return (
        <div className="account-container">
            <h2>Account Details</h2>
            {user ? (
                <div className="account-details">
                    <p>Username: {user.username}</p>
                    <p>First Name: {user.first_name}</p>
                    <p>Last Name: {user.last_name}</p>
                    <p>Email: {user.email}</p>
                    <p>Address: {user.address}</p>
                    <p>Role: {user.role}</p>

                    <h3>Delete Account</h3>
                    <p> This can not be undone</p>
                    <input 
                        type="password" 
                        className="account-input"
                        placeholder="Confirm Password" 
                        onChange={(e) => setDeletePassword(e.target.value)} 
                    />
                    <button onClick={handleDeleteAccount} className="account-button">Delete Account</button>
                </div>
            ) : (
                <p className="loading-text">Loading...</p>
            )}
        </div>
    );
};

export default Account;