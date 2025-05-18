import { useState } from 'react';
import { registerUser } from '../api';
import TextInput from './TextInput';
import RadioButtonGroup from './RadioButtonGroup';
import SelectInput from './SelectInput';
import ErrorMessage from './ErrorMessage';
import ImageInput from './ImageInput';

function RegisterForm({ onRegisterSuccess }) {
  const [userType, setUserType] = useState('customer');
  const [restaurantPreviewImage, setRestaurantPreviewImage] = useState(null);
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone_number: '',
    address: '',
    vehicle_type: '',
    license_plate: '',
    restaurant_name: '',
    restaurant_image: '',
    restaurant_address: '',
    restaurant_phone_number: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUserTypeChange = (e) => {
    setUserType(e.target.value);
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUserData(prev => ({
        ...prev,
        restaurant_image: file,
      }));
      const imageUrl = URL.createObjectURL(file);
      setRestaurantPreviewImage(imageUrl);
    } else {
      setError('請選擇有效的圖片文件');
    }
  }

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');

  if (userData.password !== userData.confirmPassword) {
    setError('兩次輸入的密碼不相同');
    setLoading(false);
    return;
  }

  userData.user_type = userType
  if (userType === 'customer') {
    userData.address = userData.address;
  } else if (userType === 'courier') {
    userData.vehicle_type = userData.vehicle_type;
    userData.license_plate = userData.license_plate;
  }

  registerUser(userData)
    .then(response => {
      if (response.error) {
        setError(response.error); // API 返回的業務錯誤（如用戶已存在）
      } else {
        onRegisterSuccess(); // 註冊成功，執行回調
      }
    })
    .catch(err => {
      setError('註冊過程中發生錯誤，請稍後再試'); // 網路錯誤或伺服器異常
      console.error('Registration error:', err);
    })
    .finally(() => {
      setLoading(false); // 無論成功或失敗，都關閉 loading
    });
};

const userTypeOptions = [
  { value: 'customer', label: '顧客' },
  { value: 'courier', label: '外送員' },
  { value: 'vendor', label: '商家' },
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
        value={userData.username}
        onChange={handleChange}
        required
      />

      <TextInput
        label="電子郵件 *"
        id="email"
        name="email"
        value={userData.email}
        onChange={handleChange}
        required
        type="email"
      />

      <TextInput
        label="密碼 *"
        id="password"
        name="password"
        value={userData.password}
        onChange={handleChange}
        required
        type="password"
      />

      <TextInput
        label="確認密碼 *"
        id="confirmPassword"
        name="confirmPassword"
        value={userData.confirmPassword}
        onChange={handleChange}
        required
        type="password"
      />

      <TextInput
        label="電話號碼"
        id="phone_number"
        name="phone_number"
        value={userData.phone_number}
        onChange={handleChange}
        type="tel"
        required
      />

      {userType === 'customer' && (
        <div className='form-group'>
          <TextInput
            label="住址"
            id="address"
            name="address"
            value={userData.address}
            onChange={handleChange}
            required
          />
        </div>
      )}

      {userType === 'courier' && (
        <>
          <SelectInput
            label="車輛類型"
            id="vehicle_type"
            name="vehicle_type"
            value={userData.vehicle_type}
            options={vehicleTypeOptions}
            onChange={handleChange}
            required
          />

          <TextInput
            label="車牌號碼"
            id="license_plate"
            name="license_plate"
            value={userData.license_plate}
            onChange={handleChange}
            required
          />
        </>
      )}

      {userType === 'vendor' && (
        <>
          <TextInput
            label="餐廳名稱"
            id="restaurant_name"
            name="restaurant_name"
            value={userData.restaurant_name}
            onChange={handleChange}
            required
          />

          <ImageInput
            label="餐廳圖片"
            id="restaurant_image"
            name="restaurant_image"
            onChange={handleImageChange}
            imagePreview={restaurantPreviewImage}
            required
          />

          <TextInput
            label="餐廳地址"
            id="restaurant_address"
            name="restaurant_address"
            value={userData.restaurant_name}
            onChange={handleChange}
            required
          />

          <TextInput
            label="餐廳電話"
            id="restaurant_phone_number"
            name="restaurant_phone_number"
            value={userData.restaurant_phone_number}
            onChange={handleChange}
            required
          />
        </>

      )}

      <button type="submit" disabled={loading}>
        {loading ? '註冊中...' : '註冊'}
      </button>
    </form>
  </div>);
}

export default RegisterForm;
