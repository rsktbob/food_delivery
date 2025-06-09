import { useState, useEffect } from 'react';
import { CustomerGetOrder, CustomerDoneOrders } from '../../api';
import DeliveryMap from '../../components/CustomerGoogleMap'
import CustomerOrderInfo from '../../components/CustomerOrderInfo'
import { useNavigate } from 'react-router-dom';

function TrackOrder({ user }) {

  const [order, setOrder] = useState({});
  useEffect(() => {
      // 定義 fetch 函式
      const fetchOrders = async () => {
        CustomerGetOrder()
        .then(data=>{setOrder(data);})
      };
  
      // 初始執行一次
      fetchOrders();
      // 每 3 秒輪詢一次
      const interval = setInterval(fetchOrders, 3000);
  
      // 清理 interval 避免記憶體洩漏
      // return () => clearInterval(interval);
  }, []); // 只在組件 mount 時執行一次
  
  const navigate = useNavigate();
  useEffect(() => {
    if(order.status === 'finish' || order.status === 'Reject'){
      navigate(`/`);
      CustomerDoneOrders(order.id)
    }
  }, [order]);
  return (
    <div className="container-fluid">
      <div className="row">
        {/* 左側：訂單列表 - 固定寬度 */}
        <div className="col-auto" style={{ width: '400px' }}>
          <CustomerOrderInfo
            selectedOrder={order}
          />
        </div>
        
        {/* 右側：地圖 - 佔剩餘全部空間 */}
        <div className="col">
          <DeliveryMap
            user={user}
            selectedOrder={order}
            initialPosition={{ lat: 25.0330, lng: 121.5654 }}
            googleMapsApiKey="AIzaSyCgoPkIvc9J-vnVbVDyYDztNTZngKPecEE"
          />
        </div>
      </div>
    
    </div>
  );
}

export default TrackOrder;