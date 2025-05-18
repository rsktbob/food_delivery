import { CourierTakeOrders } from '../api';

function CouriorOrderItem({ order, user}){
  const { id, customer_name, restaurant, distance, fee } = order;

  const handleAcceptOrder = async () => {
    const response = await CourierTakeOrders(id, user.id);
    
    const { success } = response;
    if(success == true){
      alert("成功");
    }else{
      alert("失敗");
    }
  };
  return (
    <div className="list-group-item">
      <div className="d-flex flex-column">
        <div className="mb-1">訂單編號: {id}</div>
        <div className="mb-1">客戶姓名: {customer_name}</div>
        <div className="mb-1">餐廳: {restaurant}</div>
        <div className="mb-1">距離: {distance} m</div>
        <div className="mb-2">費用: NT$ {fee}</div>
        <div className="d-flex justify-content-end">
          <button className="btn btn-primary" onClick={handleAcceptOrder}>查看詳情</button>
        </div>
      </div>
    </div>
  );
};

export default CouriorOrderItem;