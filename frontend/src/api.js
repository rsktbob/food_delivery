// 從 cookie 取出 csrf token
const getCSRFToken = () => {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return decodeURIComponent(value);
  }
  return null;
};

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
  const csrfToken = getCSRFToken();

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(userData),
    credentials: 'include',  // 包含 cookies
  });

  return response.json();
};

export const loginUser = async (credentials) => {
  const API_URL = 'http://localhost:8000/api/login/';


  const csrfToken = getCSRFToken();

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
    body: JSON.stringify(credentials),
  });

  return response.json();
}