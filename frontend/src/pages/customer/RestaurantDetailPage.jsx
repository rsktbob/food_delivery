import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { addFoodItemToCart, fetchFoodItems, fetchRestaurant } from '../../api';
import RestaurantInfo from '../../components/RestaurantInfo';
import FoodCard from '../../components/FoodCard';
import FoodCategoryCard from '../../components/FoodCategoryCard';

function RestaurantDetailPage() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState({
    name: '',
    address: '',
    image: '',
  });
  const [foodItems, setFoodItems] = useState([])

  useEffect(() => {
    fetchRestaurant(id)
    .then(data => {
      console.log(data);
      setRestaurant(data);
    })
    .catch(error => console.log(`error: ${error}`))

    fetchFoodItems(id)
    .then(data => setFoodItems(data))
    .catch(error => console.log(`error: ${error}`))

  }, [id])

  const handleAddFoodItemToCart = (foodId, quantity) => {
    addFoodItemToCart(id, foodId, quantity)
    .then(response => alert("新增食物成功"))
    .catch(error => console.log(`error: ${error}`))
  }


  return (
    <div>
      <RestaurantInfo restaurant={restaurant}/>

      
      {/* 顯示菜單項目 */}
      <div className="mt-4">
        <h3>現有餐點</h3>
        {foodItems.length === 0 ? (
          <p>暫無餐點項目</p>
        ) : (
          <div className="row">
            {foodItems.map(item => (
              <div key={item.id} className="col-md-3 mb-3">
                <FoodCard food={item} onAddToCart={handleAddFoodItemToCart}/>
                {/* <FoodCategoryCard foodItem={item}/> */}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default RestaurantDetailPage;