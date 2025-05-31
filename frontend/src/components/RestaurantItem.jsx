import React from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function RestaurantItem({ restaurant }) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/restaurants/${restaurant.id}`);
  };

  return (
    <div style={{width: "300px"}}>
    <div className="card h-100" onClick={handleClick} style={{ cursor: 'pointer' }}>
        <div className="card-body">
        <h5 className="card-title">{restaurant.name}</h5>
        <div className="text-center">
            <img 
                src={restaurant.image} 
                alt="未有餐廳圖片" 
                className="img-fluid" 
            />
        </div>
        <p className="card-text">地址:{restaurant.address}</p>
        </div>
    </div>
    </div>
  );
};

export default RestaurantItem;