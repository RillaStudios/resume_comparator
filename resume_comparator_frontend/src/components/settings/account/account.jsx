import { useEffect, useState } from 'react';
import { getProfile, changePassword, deleteAccount, logout } from '../../service/authService';
import { useNavigate } from 'react-router-dom';

const Account = () => {
    const [user, setUser] = useState(null);
    const [deletePassword, setDeletePassword] = useState('');
    const navigate = useNavigate();

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
            alert('Account deleted');
            logout();
            navigate('/login');
        } catch (err) {
            alert('Error deleting account');
        }
    };

    return (
        <div>
            <h2>Account Details</h2>
            {user ? (
                <div>
                    <p>Username: {user.username}</p>
                    <p>First Name: {user.first_name}</p>
                    <p>Last Name: {user.last_name}</p>
                    <p>Email: {user.email}</p>
                    <p>Address: {user.address}</p>
                    <p>Role: {user.role}</p>
                    
                    
                    <h3>Delete Account</h3>
                    <input type="password" 
                    placeholder="Confirm Password" 
                    onChange={(e) => setDeletePassword(e.target.value)} />
                    <button onClick={handleDeleteAccount}>Delete Account</button>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Account;
