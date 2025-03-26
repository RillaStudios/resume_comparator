import React from 'react'

const forgetPassword = () => {
const [newPassword, setNewPassword] = useState('');

const handleChangePassword = async () => {
        try {
            await changePassword(newPassword);
            alert('Password changed successfully');
        } catch (err) {
            alert('Error changing password');
        }
    };
  return (
    <div>
     <h3>Change Password</h3>
                    <input type="password" placeholder="New Password" onChange={(e) => setNewPassword(e.target.value)} />
                    <button onClick={handleChangePassword}>Change Password</button>
    </div>
  )
}

export default forgetPassword
