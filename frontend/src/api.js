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

export const CourierTakeOrders = async (id,user_id) => {
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

export const CourierPickUpMeals = async (id) => {
  const API_URL = 'http://localhost:8000/api/courier-pick-up-meals/';
  const csrfToken = getCSRFToken();
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ "order_id": id }),
    credentials: 'include',
  });

};

export const CourierFinishOrders = async (id) => {
  const API_URL = 'http://localhost:8000/api/courier-finish-orders/';
  const csrfToken = getCSRFToken();
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ "order_id": id}),
    credentials: 'include',
  });

};

export const CourierUpdatePos = async (user_id, lat, lng) => {
  const API_URL = 'http://localhost:8000/api/courier-update-pos/';
  const csrfToken = getCSRFToken();
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ 
      "user_id": user_id ,
      "pos":{
        "lat":lat,
        "lng":lng
      }
    }),
    credentials: 'include',
  });

  return await response.json();
};

export const fetchRestaurant = async (restaurantId) => {
  const API_URL = `${API_BASE_URL}/restaurants/${restaurantId}`;
  
  const response = await fetch(API_URL, {
    method: 'GET',
    credentials: 'include',
  });

  return response.json();
}
 
export const fetchFoodItems = async (restaurantId) => {
  const API_URL = `${API_BASE_URL}/restaurants/${restaurantId}/food_items/`

  const response = await fetch(API_URL, {
    method: 'GET',
    credentials: 'include'
  });
  
  if (!response.ok) {
    throw new Error('獲取菜單項目失敗');
  }
  
  return response.json();
}

export const fetchCartItems = async () => {
  const API_URL = `${API_BASE_URL}/cart_items`;

  const response = await fetch(API_URL, {
    method: 'GET',
    credentials: 'include'
  });

  if (!response.ok) {
    throw new Error('獲取購物車項目失敗');
  }

  return response.json();
}


export const AddFoodItem = async (formData) => {
  const API_URL = `${API_BASE_URL}/food_items/add`;
  const csrfToken = getCSRFToken();

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    body: formData,
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('新增餐點失敗');
  }

  return await response.json();
};

export const fetchFoodCategory = async () => {
  const API_URL = `${API_BASE_URL}/food_category`;
  const csrfToken = getCSRFToken();

  const response = await fetch(API_URL, {
    method: 'GET',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('獲取食物類別失敗');
  }

  return await response.json();

}

export const deleteFoodItem = async (foodId) => {
  const API_URL = `${API_BASE_URL}/food_items/${foodId}/delete`;
  const csrfToken = getCSRFToken();
  
  const response = await fetch(API_URL, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('刪除餐點失敗');
  }

  return await response.json();
}

export const AddFoodItemToCart = async (restaurantId, foodId, quantity) => {
  const API_URL = `${API_BASE_URL}/restaurants/${restaurantId}/cart/add`;
  const csrfToken = getCSRFToken();

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
        body: JSON.stringify({
      food_id: foodId,
      quantity: quantity,
    }),
  })

  
  if (!response.ok) {
    throw new Error('加入到購物車失敗');
  }

  return await response.json();
}

export const deleteCartItem = async (cartItemId) => {
  const API_URL = `${API_BASE_URL}/cart_items/${cartItemId}/delete`;
  const csrfToken = getCSRFToken();
  
  const response = await fetch(API_URL, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('刪除購物車中的餐點失敗');
  }

  return await response.json();
}


export const fetchRestaurants = async () => {
  const API_URL = `${API_BASE_URL}/restaurants`;
  const csrfToken = getCSRFToken();

  const response = await fetch(API_URL, {
    method: 'GET',
    headers: {
      'X-CSRFToken': csrfToken,
    },
    credentials: 'include',
  })

  
  if (!response.ok) {
    throw new Error('獲得餐廳失敗');
  }

  return await response.json();
}
