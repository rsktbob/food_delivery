import React from 'react';
import { CourierPickUpMeals, CourierFinishOrders } from '../api';
function CourierOrderInfo({ selectedOrder ,navigationStep, onNavigationStepChange}) {

  return (
    <div className="card">
      <div className="card-header">
        <h5 className="card-title mb-0">訂單資訊</h5>
      </div>
      
      <div className="card-body" style={{ height: '80vh', overflowY: 'auto' }}>
        <div className="mb-3">
          <strong>訂單編號：</strong>{selectedOrder.id}
        </div>
        <div className="mb-3">
          <strong>客戶姓名：</strong>{selectedOrder.customer}
        </div>
        <div className="mb-3">
          <strong>餐廳：</strong>{selectedOrder.restaurant.name}
        </div>
        <div className="mb-3">
          <strong>距離：</strong>{selectedOrder.distance} m
        </div>
        <div className="mb-4">
          <strong>費用：</strong>NT$ {selectedOrder.fee}
        </div>
        
        {navigationStep === 1 && (
          <button className="btn btn-success w-100" onClick={() => {onNavigationStepChange(2); CourierPickUpMeals(selectedOrder.id)}}>
            完成取餐
          </button>
        )}
        
        {navigationStep === 3 && (
          <button className="btn btn-warning w-100" onClick={() => {onNavigationStepChange(4); CourierFinishOrders(selectedOrder.id)}}>
            完成配送
          </button>
        )}
      </div>
    </div>
  );
}

export default CourierOrderInfo;