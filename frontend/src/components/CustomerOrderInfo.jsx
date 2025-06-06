import { useState,useEffect } from "react";

function CourierOrderInfo({ selectedOrder }) {
  const [orderItems, setOrderItems] = useState([]);
  useEffect(() => {
      console.log("Order updated:", selectedOrder);
      setOrderItems(selectedOrder?.items || [])
    }, [selectedOrder]);

  // 訂單狀態配置
  const orderStates = [
    { id: 1, name: '已創建', completed: false },
    { id: 2, name: '開始製作', completed: false },
    { id: 3, name: '已接單', completed: false },
    { id: 4, name: '已取餐', completed: false },
    { id: 5, name: '已送達', completed: false }
  ];

  // 根據訂單狀態更新進度
  const updateOrderStates = (currentState) => {
    return orderStates.map(state => ({
      ...state,
      completed: state.id <= currentState
    }));
  };

  // 將字串狀態轉換為數字
  const getStatusNumber = (status) => {
    switch(status) {
      case 'Created': return 1;
      case 'Accepted': return 2;
      case 'Assigned': return 3;
      case 'Picked_Up': return 4;
      case 'Finish': return 5;
      default: return 1;
    }
  };

  const currentStates = updateOrderStates(getStatusNumber(selectedOrder?.status));

  // 固定的費用資料（測試用）
  const deliveryFee = 35;
  const subtotal = orderItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const total = subtotal + deliveryFee;

  return (
    <div className="card">
      <div className="card-header">
        <h5 className="card-title mb-0">訂單資訊</h5>
      </div>
      
      <div className="card-body" style={{ height: '80vh', overflowY: 'auto' }}>
        {/* 訂單狀態進度條 */}
        <div className="mb-4">
          <div className="d-flex justify-content-between">
            {currentStates.map((state, index) => (
              <div key={state.id} className="text-center" style={{ flex: 1 }}>
                <div className={`rounded-circle d-flex align-items-center justify-content-center mb-2 mx-auto ${
                  state.completed ? 'bg-success text-white' : 'bg-light text-muted'
                }`} style={{ width: '40px', height: '40px' }}>
                  {state.id}
                </div>
                <small className={state.completed ? 'text-success fw-bold' : 'text-muted'}>
                  {state.name}
                </small>
                {index < currentStates.length - 1 && (
                  <div className={`position-absolute ${
                    state.completed ? 'bg-success' : 'bg-light'
                  }`} style={{ 
                    height: '2px', 
                    width: 'calc(100% / 5)',
                    top: '20px',
                    left: `${(index + 1) * 20}%`,
                    zIndex: -1
                  }}></div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* 基本訂單資訊 */}
        <div className="mb-3">
          <strong>訂單編號：</strong>{selectedOrder?.id || 'A001'}
        </div>
        <div className="mb-3">
          <strong>客戶姓名：</strong>{selectedOrder?.customer || '王小明'}
        </div>
        <div className="mb-3">
          <strong>餐廳：</strong>{selectedOrder?.restaurant?.name || '美味餐廳'}
        </div>

        {/* 訂單品項 */}
        <div className="mb-4">
          <h6 className="fw-bold mb-3">訂單品項</h6>
          <div className="border rounded p-3">
            {orderItems.map((item, index) => (
                <div key={index} className="d-flex justify-content-between align-items-center mb-2">
                    <div>
                    <span className="fw-bold">{item.food_name}</span>
                    <span className="text-muted ms-2">x {item.quantity}</span>
                    </div>
                    <span className="fw-bold">NT$ {parseFloat(item.food_price) * item.quantity}</span>
                </div>
            ))}
            
            {/* 分隔線 */}
            <hr className="my-3" />
            
            {/* 小計 */}
            <div className="d-flex justify-content-between mb-2">
              <span>小計</span>
              <span>NT$ {subtotal}</span>
            </div>
            
            {/* 外送費 */}
            <div className="d-flex justify-content-between mb-2">
              <span>外送費</span>
              <span>NT$ {selectedOrder.delivery_fee}</span>
            </div>
            
            {/* 總計 */}
            <hr className="my-2" />
            <div className="d-flex justify-content-between">
              <span className="fw-bold fs-5">總計</span>
              <span className="fw-bold fs-5 text-primary">NT$ {selectedOrder.total_price}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default CourierOrderInfo;