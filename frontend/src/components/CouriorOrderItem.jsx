import { CourierTakeOrders } from '../api';

function CourierOrderItem({ 
  order, 
  user, 
  isSelected = false,   // 新增：是否被選中
  onShowDetails,        // 顯示詳情回調
  onStartNavigation,    // 開始導航回調
}) {

  // 處理接單
  const handleAcceptOrder = async () => {
    try {
      const response = await CourierTakeOrders(order.id, user.id);
      const { success } = response;
      
      if (success === true) {
        alert("成功接單");
        // 接單成功後自動開始導航
        if (onStartNavigation) {
          onStartNavigation(order);
        }
      } else {
        alert("接單失敗");
      }
    } catch (error) {
      console.error('接單時發生錯誤:', error);
      alert("接單失敗，請稍後再試");
    }
  };

  // 處理顯示詳情
  const handleShowDetails = () => {
    if (onShowDetails) {
      onShowDetails(order);
    }
  };

  return (
    <div className={`list-group-item ${isSelected ? 'list-group-item-primary' : ''}`}>
      <div className="d-flex flex-column">
        <div className="mb-1">
          <strong>訂單編號:</strong> {order.id}
        </div>
        <div className="mb-1">
          <strong>客戶姓名:</strong> {order.customer}
        </div>
        <div className="mb-1">
          <strong>餐廳:</strong> {order.restaurant}
        </div>
        <div className="mb-1">
          <strong>距離:</strong> {order.distance} km
        </div>
        
        <div className="d-flex justify-content-end gap-2">
          {/* 顯示詳情按鈕 */}
          <button 
            className={`btn btn-sm ${isSelected ? 'btn-outline-light' : 'btn-outline-primary'}`}
            onClick={handleShowDetails}
            title="在地圖上查看此訂單的詳細位置"
          >
            查看詳情
          </button>
          
          {/* 顯示接單按鈕 */}
          <button 
            className="btn btn-sm btn-primary" 
            onClick={handleAcceptOrder}
            title="接受此訂單並開始導航"
          >
            接受訂單
          </button>
          
        </div>
      </div>
    </div>
  );
}

export default CourierOrderItem;