import { useState } from 'react';
import { loginUser } from '../api';
import TextInput from './TextInput';

function LoginForm({ onLoginSuccess }) {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await loginUser(credentials);
      
      if (response.error) {
        setError(response.error);
      } else {
        // 登入成功，通知父組件
        onLoginSuccess(response);
      }
    } catch (err) {
      setError('登入過程中發生錯誤，請稍後再試');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-form">
      <h2>登入</h2>
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <TextInput
          label="用戶名"
          id="username"
          name="username"
          value={credentials.username}
          onChange={handleChange}
          required
        />

        <TextInput
          label="密碼"
          id="password"
          name="password"
          value={credentials.password}
          onChange={handleChange}
          type="password"
          required
        />

        
        <button type="submit" disabled={loading}>
          {loading ? '登入中...' : '登入'}
        </button>
      </form>
    </div>
  );
};

export default LoginForm;