// 保留原有功能
export const getHelloWorld = async () => {
  const API_URL = 'http://localhost:8000/hello/';
  const response = await fetch(API_URL);
  const data = await response.json();
  return data.message;
};

export const getOrderById = async (orderId) => {
  const API_URL = 'http://localhost:8000/order';
  const response = await fetch(`${API_URL}/${orderId}/`);
  const data = await response.json();
  
  return data;
};

// 添加登入/註冊功能
export const registerUser = async (userData) => {
  const API_URL = 'http://localhost:8000/api/register/';
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
    credentials: 'include',  // 包含 cookies
  });
  
  return response.json();
};

export const loginUser = async (credentials) => {
  const API_URL = 'http://localhost:8000/api/login/';
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(credentials),
    credentials: 'include',  // 包含 cookies
  });
  
  return response.json();
};