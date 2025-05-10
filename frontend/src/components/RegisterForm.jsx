import { useState } from 'react';
import { registerUser } from '../api';
import TextInput from './TextInput';
import RadioButtonGroup from './RadioButtonGroup';
import SelectInput from './SelectInput';
import ErrorMessage from './ErrorMessage';

function RegisterForm({ onRegisterSuccess }) {
  const [userType, setUserType] = useState('customer');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone_number: '',
    address: '',
    vehicle_type: '',
    license_plate: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUserTypeChange = (e) => setUserType(e.target.value);

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

    if (formData.password !== formData.confirmPassword) {
      setError('兩次輸入的密碼不相同');
      setLoading(false);
      return;
    }

    const userData = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      phone_number: formData.phone_number,
      user_type: userType,
    };

    if (userType === 'customer') {
      userData.address = formData.address;
    } else if (userType === 'courier') {
      userData.vehicle_type = formData.vehicle_type;
      userData.license_plate = formData.license_plate;
    }

    try {
      const response = await registerUser(userData);

      if (response.error) {
        setError(response.error);
      } else {
        onRegisterSuccess();
      }
    } catch (err) {
      setError('註冊過程中發生錯誤，請稍後再試');
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  const userTypeOptions = [
    { value: 'customer', label: '顧客' },
    { value: 'courier', label: '快遞員' },
    { value: 'vendor', label: '廠商' },
  ];

  const vehicleTypeOptions = [
    { value: '機車', label: '機車' },
    { value: '汽車', label: '汽車' },
    { value: '自行車', label: '自行車' },
  ]

  return (
    <div className="register-form">
      <h2>註冊新帳號</h2>
      <ErrorMessage error={error} />

      <form onSubmit={handleSubmit}>
        <div className='form-group'>
          <label>用戶類型</label>
          <RadioButtonGroup
            options={userTypeOptions}
            selectedValue={userType}
            onChange={handleUserTypeChange}
          />
        </div>

        <TextInput
          label="用戶名 *"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <TextInput
          label="電子郵件 *"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          type="email"
        />

        <TextInput
          label="密碼 *"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          type="password"
        />

        <TextInput
          label="確認密碼 *"
          id="confirmPassword"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          type="password"
        />

        <TextInput
          label="電話號碼"
          id="phone_number"
          name="phone_number"
          value={formData.phone_number}
          onChange={handleChange}
          type="tel"
        />

        {userType === 'customer' && (
          <div className='form-group'>
            <TextInput
              label="住址"
              id="address"
              name="address"
              value={formData.address}
              onChange={handleChange}
            />
          </div>
        )}

        {userType === 'courier' && (
          <>
            <SelectInput
              label="車輛類型"
              id="vehicle_type"
              name="vehicle_type"
              value={formData.vehicle_type}
              options={vehicleTypeOptions}
              onChange={handleChange}
            />

            <TextInput
              label="車牌號碼"
              id="license_plate"
              name="license_plate"
              value={formData.license_plate}
              onChange={handleChange}
            />
          </>
        )}

        <button type="submit" disabled={loading}>
          {loading ? '註冊中...' : '註冊'}
        </button>
      </form>
    </div>
  );
}

export default RegisterForm;
