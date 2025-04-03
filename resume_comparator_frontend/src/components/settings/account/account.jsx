import { useEffect, useState } from 'react';
import { getProfile, deleteAccount, logout } from '../../service/authService';
import { toast } from 'react-toastify';
import ProfilePic from '../../../assets/image/profilePic.png';
import ForgetPassword from '../forgetPassword/forgetPassword'; 
import './Account.css'; 
import spinner from "../../../assets/image/loadingSpinner.gif";
import { useNavigate } from 'react-router-dom';

const Account = () => {
    const [user, setUser] = useState(null);
    const [deletePassword, setDeletePassword] = useState('');
    const [showChangePassword, setShowChangePassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false); // State for modal
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUser = async () => {
            setLoading(true);
            try {
                const response = await getProfile();
                setUser(response.data);
            } catch (err) {
                console.error('Failed to fetch profile');
            } finally {
                setLoading(false);
            }
        };
        fetchUser();
    }, []);

    const handleDeleteAccount = async () => {
        if (!deletePassword) {
            toast.error('Please enter your password to confirm deletion');
            return;
        }

        setLoading(true);
        try {
            await deleteAccount(deletePassword);
            toast.success('Account deleted successfully');
            logout();
            // window.location.href = '/login';
            navigate('/login');
        } catch (err) {
            toast.error('Error deleting account invalid password');
        } finally {
            setLoading(false);
            setShowDeleteModal(false); // Close modal after deletion
        }
    };

    return (
        <div className="account-container">
            <div className="hero-image">
                <img src={ProfilePic} alt="Profile" />
            </div>

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

                    <div className="delete-section">
                        <h3>Delete Account</h3>
                        <p>This action cannot be undone.</p>
                        <input 
                            type="password" 
                            className="account-input"
                            placeholder="Confirm Password" 
                            onChange={(e) => setDeletePassword(e.target.value)} 
                        />
                        <button onClick={() => setShowDeleteModal(true)} className="account-button">
                            Delete Account
                        </button>

                        

                        <a href="#" className="change-password" onClick={() => setShowChangePassword(true)}>Change Password Here</a>
                    </div>
                </>
            ) : (
                <p className="loading-text">Loading...</p>
            )}

            {showChangePassword && <ForgetPassword onClose={() => setShowChangePassword(false)} />}

            {/* Delete Confirmation Modal */}
            {showDeleteModal && (
                <div className="modal-overlay">
                    <div className="modal">
                        <h3>Are you sure you want to delete your account?</h3>
                        <p>It's sad to see you go. This action cannot be undone.</p>
                        <div className="modal-buttons">
                            <button onClick={handleDeleteAccount} className="confirm-delete">Yes, Delete</button>
                            <button onClick={() => setShowDeleteModal(false)} className="cancel-delete">No, Cancel</button>
                        </div>
                    </div>
                </div>
            )}
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

export default Account;
