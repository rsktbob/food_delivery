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


const API_BASE_URL = 'http://localhost:8000/api';

// 添加登入/註冊功能
export const registerUser = async (userData) => {
  const API_URL = `${API_BASE_URL}/register/`;
  const csrfToken = getCSRFToken();
  
  const formData = new FormData();

  // 添加所有字段到 formData
  Object.keys(userData).forEach(key => {
    formData.append(key, userData[key]);
  });

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    body: formData,
    credentials: 'include',  // 包含 cookies
  });

  return response.json();
};

export const loginUser = async (credentials) => {
  const API_URL = `${API_BASE_URL}/login/`;
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

export const CourierCheckOrders = async () => {
  const API_URL = 'http://localhost:8000/api/courier-check-orders/';
  const csrfToken = getCSRFToken();
  const response = await fetch(API_URL, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
  });

  return await response.json();
};

export const CourierTakeOrders = async (id,user_id) => {
  console.log(user_id)
  const API_URL = 'http://localhost:8000/api/courier-take-orders/';
  const csrfToken = getCSRFToken();
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ "order_id": id , "user_id": user_id}),
    credentials: 'include',
  });

  return await response.json();
};
export const fetchRestaurantInfo = async () => {
  const API_URL = `${API_BASE_URL}/restaurant/`;
  
  const response = await fetch(API_URL, {
    method: 'GET',
    credentials: 'include',
  });

  return response.json();
}

export const fetchMenuItems = async () => {
  const API_URL = `${API_BASE_URL}/menu_items/`

  const response = await fetch(API_URL, {
    method: 'GET',
    credentials: 'include'
  });
  
  if (!response.ok) {
    throw new Error('獲取菜單項目失敗');
  }
  
  return response.json();
}


export const AddMenuItem = async () => {
  const API_URL = `${API_BASE_URL}/menu_items/add`
  const csrfToken = getCSRFToken()

  
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'X-CSRFtoken': csrfToken,
    },
    body: {

    },
    credentials: 'include'
  })

  if (!response.ok) {
    throw new Error("新增餐點失敗")
  }
}
