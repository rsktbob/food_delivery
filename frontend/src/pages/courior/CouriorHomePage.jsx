import { useState } from 'react';
import CouriorOrderList from '../../components/CourierOrderList';
import CourierOrderInfo from '../../components/CourierOrderInfo';
import DeliveryMap from '../../components/CourierGoogleMap'

function CouriorHomePage({ user }) {
  // 管理選中的訂單
  const [selectedOrder, setSelectedOrder] = useState(null);
  // 管理導航狀態
  const [isNavigating, setIsNavigating] = useState(false);
  // 統一的導航步驟管理 - 作為單一真實來源
  const [navigationStep, setNavigationStep] = useState(0);

  // 處理顯示訂單詳情
  const handleShowOrderDetails = (order) => {
    console.log('顯示訂單詳情:', order);
    setSelectedOrder(order);
    setIsNavigating(false);
    setNavigationStep(0); // 重置導航步驟
  };

  // 處理開始導航（接單後）
  const handleStartNavigation = (order) => {
    console.log('開始導航到:', order);
    setSelectedOrder(order);
    setIsNavigating(true);
    // 不在這裡設置步驟，讓 DeliveryMap 組件來控制
    // 這樣避免重複設置和不同步問題
  };

  // 處理導航開始回調
  const handleNavigationStart = (type, target) => {
    console.log('導航開始:', type, target);
    if (type === 'restaurant') {
      console.log('前往餐廳:', target.name);
    } else if (type === 'customer') {
      console.log('前往顧客:', target);
    }
  };

  // 處理導航結束回調
  const handleNavigationEnd = (order) => {
    console.log('導航結束，訂單完成:', order);
    setSelectedOrder(null);
    setIsNavigating(false);
    setNavigationStep(0);
    alert(`訂單 ${order.id} 配送完成！`);
  };

  // 統一處理導航步驟變化 - 作為單一真實來源
  const handleNavigationStepChange = (step) => {
    console.log('導航步驟變化:', step);
    setNavigationStep(step);
    
    const stepMessages = {
      0: '等待接單',
      1: '前往餐廳取餐',
      2: '取餐',
      3: '前往顧客送餐',
      4: '完成',
    };
    
    if (stepMessages[step]) {
      console.log('當前狀態:', stepMessages[step]);
    }
  };

  // 處理外送員位置變化（可選）
  const handleDeliveryPositionChange = (position) => {
    // 可以在這裡處理位置變化，例如發送到後端
    // console.log('外送員位置更新:', position);
  };

  return (
    <div className="container-fluid">
      <div className="row">
        {/* 左側：訂單列表 - 固定寬度 */}
        <div className="col-auto" style={{ width: '400px' }}>
          {navigationStep === 0 ? 
          <CouriorOrderList
            user={user}
            selectedOrder={selectedOrder}
            onShowOrderDetails={handleShowOrderDetails}
            onStartNavigation={handleStartNavigation}
          /> 
          :
          <CourierOrderInfo 
            selectedOrder={selectedOrder}
            navigationStep={navigationStep}
            onNavigationStepChange={handleNavigationStepChange}
          />
          }
        </div>
        
        {/* 右側：地圖 - 佔剩餘全部空間 */}
        <div className="col">
          <DeliveryMap
            user={user}
            selectedOrder={selectedOrder}
            isNavigating={isNavigating}
            navigationStep={navigationStep} // 傳遞當前步驟
            onNavigationStart={handleNavigationStart}
            onNavigationEnd={handleNavigationEnd}
            onNavigationStepChange={handleNavigationStepChange} // 讓地圖組件更新父組件狀態
            onDeliveryPositionChange={handleDeliveryPositionChange}
            initialPosition={{ lat: 25.0330, lng: 121.5654 }}
            googleMapsApiKey="AIzaSyCgoPkIvc9J-vnVbVDyYDztNTZngKPecEE"
          />
        </div>
      </div>
      
      {/* 可選：顯示當前狀態 */}
      {selectedOrder && (
        <div className="position-fixed bottom-0 start-0 m-3 p-3 bg-dark text-white rounded">
          <div>當前訂單: {selectedOrder.id}</div>
          <div>狀態: {
            navigationStep === 0 ? '查看詳情' :
            navigationStep === 1 ? '前往餐廳' :
            navigationStep === 2 ? '前往顧客' : '未知'
          }</div>
          {isNavigating && (
            <div className="text-warning">🚗 導航中...</div>
          )}
        </div>
      )}
    </div>
  );
}

export default CouriorHomePage;