import CouriorOrderItem from './CouriorOrderItem'
import { CourierCheckOrders } from '../api';
import { useState, useEffect } from 'react';
function CouriorOrderList({user}){

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

    return(
        <div className="customer-dashboard">
            <h2>外送員主頁</h2>
            <div className="container mt-4">
                <h2 className="mb-4">訂單列表</h2>
                <div className="card">
                    <div className="card-body p-0">
                    <div className="list-group list-group-flush">
                        {orders.map(order => (
                            <CouriorOrderItem key={order.id} order={order} user={user}/>
                        ))}
                    </div>
                    </div>
                </div>
            </div>

        </div>
    )
}

export default CouriorOrderList;