import { fetchMenuItems } from "../../api";
import React, { useState, useEffect } from "react";
import MenuItem from "../../components/Menutem";

function ReviseMenuPage({ user }) {
  const [menuItems, setMenuItems] = useState([]);
  const [refresh, setRefresh] = useState(false);

  useEffect(() => {
    fetchMenuItems()
      .then(data => {
        console.log(data);
        setMenuItems(data);
      })
  }, [refresh]);


  const handleMenuItemAdded = () => {
    setRefresh(prev => !prev);
  };

  return (
    <div className="container py-5">
      <h2 className="display-4">修改餐點</h2>

      <button className="btn btn-primary" onClick={handleMenuItemAdded}>新增餐點</button>      

      {/* 顯示菜單項目 */}
      <div className="mt-4">
        <h3>現有餐點</h3>
        {menuItems.length === 0 ? (
          <p>暫無餐點項目</p>
        ) : (
          <div className="row">
            {menuItems.map(item => (
              <div key={item.id} className="col-md-4 mb-3">
                <MenuItem food={item}/>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ReviseMenuPage