import React, { useState } from 'react';
import VendorOrderItem from './VendorOrderItem'; // 假設你是這樣 import
import { restaurantAcceptOrder, restaurantRejectOrder } from '../api';


function VendorOrderList({ orders, setOrders }) {

  // 處理接受訂單
  const handleAccept = (orderId) => {
    console.log('接受訂單', orderId);
    setOrders(prev =>
      prev.map(o => (o.id === orderId ? { ...o, status: 'accepted' } : o))
    );
    restaurantAcceptOrder(orderId);
  };

  // 處理拒絕訂單
  const handleReject = (orderId) => {
    console.log('拒絕訂單', orderId);
    setOrders(prev => prev.filter(o => o.id !== orderId));
    restaurantRejectOrder(orderId);
  };

  return (
  <div className="card border h-100 d-flex flex-column">
    <div className="card-header bg-light">
      <h5 className="card-title mb-0">訂單列表</h5>
    </div>

    <div className="card-body p-0 flex-grow-1 overflow-auto" style={{height: '80vh'}}>
      <div className="list-group list-group-flush">
        {orders.map(order => (
          <VendorOrderItem 
            key={order.id} 
            order={order} 
            onAccept={handleAccept}
            onReject={handleReject}
          />
        ))}
      </div>
    </div>
  </div>
  );
}

export default VendorOrderList;
