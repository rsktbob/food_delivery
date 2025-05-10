import { useState } from 'react';
import LoginForm from '../components/LoginForm';
import RegisterForm from '../components/RegisterForm';

const AuthPage = ({ onUserAuthenticated }) => {
  const [isLoginMode, setIsLoginMode] = useState(true);
  
  const handleLoginSuccess = (userData) => {
    // 將用戶信息傳遞給父組件
    onUserAuthenticated(userData);
  };
  
  const handleRegisterSuccess = () => {
    // 註冊成功後切換到登入模式
    setIsLoginMode(true);
    alert('註冊成功！請使用您的新帳號登入。');
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>食物外送系統</h1>
          <div className="auth-tabs">
            <button
              className={`tab-button ${isLoginMode ? 'active' : ''}`}
              onClick={() => setIsLoginMode(true)}
            >
              登入
            </button>
            <button
              className={`tab-button ${!isLoginMode ? 'active' : ''}`}
              onClick={() => setIsLoginMode(false)}
            >
              註冊
            </button>
          </div>
        </div>
        
        <div className="auth-content">
          {isLoginMode ? 
            <LoginForm onLoginSuccess={handleLoginSuccess} />
           : 
            <RegisterForm onRegisterSuccess={handleRegisterSuccess} />
          }
        </div>
      </div>
    </div>
  );
};

export default AuthPage;