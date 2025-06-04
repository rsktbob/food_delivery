import CouriorOrderItem from './VendorOrderItem'
import { CourierCheckOrders } from '../api';
import { useState, useEffect } from 'react';

function CouriorOrderList({ 
  user, 
  selectedOrder,        // 新增：當前選中的訂單
  onShowOrderDetails,   // 新增：顯示訂單詳情回調
  onStartNavigation     // 新增：開始導航回調
}) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    // 定義 fetch 函式
    const fetchOrders = async () => {
      const data = await CourierCheckOrders();
      setOrders(data);
    };

    // 初始執行一次
    fetchOrders();

    // 每 3 秒輪詢一次
    const interval = setInterval(fetchOrders, 3000);

    // 清理 interval 避免記憶體洩漏
    return () => clearInterval(interval);
  }, []); // 只在組件 mount 時執行一次

  return (
    <div className="card border">
      <div className="card-header bg-light">
        <h5 className="card-title mb-0">訂單列表</h5>
        {selectedOrder && (
          <small className="text-muted">
            已選擇訂單: {selectedOrder.id}
          </small>
        )}
      </div>
      <div className="card-body p-0" style={{ height: '80vh', overflowY: 'auto' }}>
        <div className="list-group list-group-flush">
          {orders.map(order => (
            <CouriorOrderItem 
              key={order.id} 
              order={order} 
              user={user}
              isSelected={selectedOrder?.id === order.id} // 新增：是否被選中
              onShowDetails={onShowOrderDetails}          // 傳遞回調
              onStartNavigation={onStartNavigation}       // 傳遞回調
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export default CouriorOrderList;