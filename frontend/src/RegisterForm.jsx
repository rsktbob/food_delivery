import { useState } from 'react';
import { registerUser } from './api';

const RegisterForm = ({ onRegisterSuccess }) => {
  const [userType, setUserType] = useState('customer');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone_number: '',
    // 顧客特有欄位
    address: '',
    // 快遞員特有欄位
    vehicle_type: '',
    license_plate: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUserTypeChange = (e) => {
    setUserType(e.target.value);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    // 密碼確認檢查
    if (formData.password !== formData.confirmPassword) {
      setError('兩次輸入的密碼不相同');
      setLoading(false);
      return;
    }
    
    // 準備要發送的數據
    const userData = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      phone_number: formData.phone_number,
      user_type: userType,
    };
    
    // 根據用戶類型添加不同字段
    if (userType === 'customer') {
      userData.address = formData.address;
    } else if (userType === 'courier') {
      userData.vehicle_type = formData.vehicle_type;
      userData.license_plate = formData.license_plate;
    }
    // 廠商沒有額外字段
    
    try {
      const response = await registerUser(userData);
      
      if (response.error) {
        setError(response.error);
      } else {
        // 註冊成功
        onRegisterSuccess();
      }
    } catch (err) {
      setError('註冊過程中發生錯誤，請稍後再試');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-form">
      <h2>註冊新帳號</h2>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>用戶類型</label>
          <div className="user-type-selector">
            <label>
              <input
                type="radio"
                name="user_type"
                value="customer"
                checked={userType === 'customer'}
                onChange={handleUserTypeChange}
              />
              顧客
            </label>
            <label>
              <input
                type="radio"
                name="user_type"
                value="courier"
                checked={userType === 'courier'}
                onChange={handleUserTypeChange}
              />
              快遞員
            </label>
            <label>
              <input
                type="radio"
                name="user_type"
                value="vendor"
                checked={userType === 'vendor'}
                onChange={handleUserTypeChange}
              />
              廠商
            </label>
          </div>
        </div>
        
        {/* 共用的欄位 */}
        <div className="form-group">
          <label htmlFor="username">用戶名 *</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="email">電子郵件 *</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">密碼 *</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="confirmPassword">確認密碼 *</label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="phone_number">電話號碼</label>
          <input
            type="tel"
            id="phone_number"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
          />
        </div>
        
        {/* 顧客特有欄位 */}
        {userType === 'customer' && (
          <div className="form-group">
            <label htmlFor="address">住址</label>
            <input
              type="text"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
            />
          </div>
        )}
        
        {/* 快遞員特有欄位 */}
        {userType === 'courier' && (
          <>
            <div className="form-group">
              <label htmlFor="vehicle_type">車輛類型</label>
              <select
                id="vehicle_type"
                name="vehicle_type"
                value={formData.vehicle_type}
                onChange={handleChange}
              >
                <option value="">請選擇</option>
                <option value="機車">機車</option>
                <option value="汽車">汽車</option>
                <option value="自行車">自行車</option>
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="license_plate">車牌號碼</label>
              <input
                type="text"
                id="license_plate"
                name="license_plate"
                value={formData.license_plate}
                onChange={handleChange}
              />
            </div>
          </>
        )}
        
        <button type="submit" disabled={loading}>
          {loading ? '註冊中...' : '註冊'}
        </button>
      </form>
    </div>
  );
};

export default RegisterForm;