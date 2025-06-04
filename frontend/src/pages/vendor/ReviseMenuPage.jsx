import React, { useState, useEffect } from "react";
import {addFoodItem, fetchFoodItems, fetchFoodCategory, fetchRestaurant, deleteFoodItem}  from "../../api";
import MenuItem from "../../components/MenuItem";
import AddFoodModal from "../../components/AddFoodModel";

function ReviseMenuPage({ user }) {
  // 狀態宣告
  const [foodItems, setFoodItems] = useState([]);
  const [refresh, setRefresh] = useState(false);
  const [showAddFoodModal, setShowAddFoodModal] = useState(false);
  const [restaurant, setRestaurant] = useState({
        name: '',
        address: '',
        image_url: '',
    });

  // 載入菜單，refresh 改變時會重新載入
  useEffect(() => {
    fetchFoodItems(user.restaurant_id)
      .then(data => setFoodItems(data))
      .catch(err => console.error("載入菜單失敗:", err));
  }, [refresh]);

  // 載入餐丁，第一次渲染時呼叫
  useEffect(() => {
    fetchRestaurant(user.restaurant_id)
      .then(data => setRestaurant(data))
      .catch(err => console.error("載入餐廳失敗:", err));
  }, []);


  // 控制 Modal 顯示與隱藏
  const handleShowFoodModal = () => setShowAddFoodModal(true);
  const handleModalClose = () => setShowAddFoodModal(false);
  const handleFoodItemDelete = (id) => {
    deleteFoodItem(id)
    .then(response => {
      alert(response);
      setRefresh(prev => !prev);
    })
    .catch(err => alert("刪除食物失敗:", err));
  }

  // 新增餐點的處理
  const handleAddFood = async (formData) => {
    addFoodItem(formData)
    .then(response => {
      alert(response.message);
      setShowAddFoodModal(false);
      setRefresh(prev => !prev);
    })
    .catch(err => {
      console.error("新增餐點失敗:", err);
      alert("新增餐點失敗，請稍後再試");
    })
  };

  return (
    <div>
      <h2 className="display-4">修改餐點</h2>
      
      <button className="btn btn-primary" onClick={handleShowFoodModal}>
        新增餐點
      </button>

      {/* 顯示菜單項目 */}
      <div className="mt-4">
        <h3>現有餐點</h3>
        {foodItems.length === 0 ? (
          <p>暫無餐點項目</p>
        ) : (
          <div className="row">
            {foodItems.map(item => (
              <div key={item.id} className="col-md-3 mb-3">
                <MenuItem food={item} onDelete={handleFoodItemDelete}/>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 新增餐點 Modal */}
      <AddFoodModal
        show={showAddFoodModal}
        onClose={handleModalClose}
        onConfirm={handleAddFood}
        restaurantId={restaurant.id}
      />
    </div>
  );
}

export default ReviseMenuPage;
