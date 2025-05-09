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