import { useState, useEffect } from "react";
import { getHelloWorld, getOrderById } from './api';

function App() {
  const [message, setMessage] = useState('');
  const [order, setOrder] = useState(null);

  // 載入 Hello World 訊息
  useEffect(() => {
    const fetchMessage = async () => {
      const helloMessage = await getHelloWorld();
      setMessage(helloMessage);
    };
    fetchMessage();
  }, []);

  // 載入訂單資料
  useEffect(() => {
    const fetchOrder = async () => {
      const orderData = await getOrderById(1); // 假設訂單 ID 是 1
      setOrder(orderData);
    };

    fetchOrder();
  }, []);

  return (
    <div>
      <h1>{message}</h1>  {/* 顯示 API 回傳的 Hello World 訊息 */}
      
      {order ? (
        <div>
          <h2>訂單編號: {order.order_id}</h2>
          <p>狀態: {order.status}</p>
        </div>
      ) : (
        <p>訂單資料載入中...</p>
      )}
    </div>
  );
}

export default App;
