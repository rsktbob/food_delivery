import RestaurantInfo from "../../components/RestaurantInfo"
import { useState, useEffect } from "react"
import {fetchRestaurant, fetchRestaurantOrders} from "../../api";
import VendorOrderList from "../../components/VendorOrderList";

function VendorHomePage({user}){
    const [restaurant, setRestaurant] = useState({
        id: '',
        name: '',
        address: '',
        image: '',
    });

    const [orders, setOrders] = useState([]);

    useEffect(() => {
        fetchRestaurant(user.restaurant_id)
        .then(data => {
            setRestaurant(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })
    }, []);

    useEffect(() => {
        const fetchOrders = () => {
        if (restaurant.id) {
            fetchRestaurantOrders(restaurant.id)
            .then(data => setOrders(data))
            .catch(error => console.log(`error: ${error}`));
        }
        };

        fetchOrders(); // 先抓一次訂單

        const intervalId = setInterval(fetchOrders, 3000);

        // 清除定時器，避免記憶體洩漏
        return () => clearInterval(intervalId);
    }, [restaurant.id]);



    return(
    <div className="container-fluid">
        <div className="row">
            {/* 左側：訂單列表 */}
            <div className="col-auto" style={{ width: '400px' }}>
                <VendorOrderList orders={orders} setOrders={setOrders} />
            </div>

            {/* 右側：RestaurantInfo 滿版 */}
            <div className="col">
                <RestaurantInfo restaurant={restaurant} />
            </div>
        </div>
    </div>
    )
}

export default VendorHomePage