import { useState, useEffect } from "react"
import { fetchRestaurants } from "../../api";
import RestaurantItem from "../../components/RestaurantItem";


function CustomerHomePage({user}){
    const [restaurants, setRestaurants] = useState([]);

    useEffect(() => {
        fetchRestaurants()
        .then(data => {
            console.log(data);
            setRestaurants(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })
    }, []);
    

    return(
         <div className="container py-5">
            <h2>顧客主頁</h2>
            <p>您的地址: {user?.address || '未設定'}</p>

            <hr className="my-4" style={{ borderTop: '2px solid #333' }} />
            
            {/* 顯示菜單項目 */}
            <div className="mt-4">
                {restaurants.length === 0 ? (
                <p>暫無餐廳</p>
                ) : (
                <div className="row">
                    {restaurants.map(item => (
                    <div key={item.id} className="col-md-4 mb-3">
                        <RestaurantItem restaurant={item}/>
                    </div>
                    ))}
                </div>
                )}
            </div>
        </div>
    )
}

export default CustomerHomePage