import { useState } from "react";

function FoodCard({ food, onAddToCart }) {
  const [quantity, setQuantity] = useState(1);

  const handleAdd = () => {
    if (quantity > 0) {
      console.log(quantity);
      onAddToCart(food.id, quantity);
    }
  };

  return (
    <div className="card">
      {food.image && (
        <img
          src={food.image}
          className="card-img-top"
          alt={food.name}
          style={{ height: "200px", objectFit: "cover" }}
        />
      )}
      <div className="card-body">
        <h5 className="card-title">{food.name}</h5>
        <p className="card-text">${food.price}</p>
        
        <div className="d-flex align-items-center justify-content-between mt-2">
        <div className="d-flex align-items-center">
            <label className="me-2">數量：</label>
            <input
            type="number"
            min="1"
            value={quantity}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            className="form-control"
            style={{ width: "80px" }}
            />
        </div>

        <button className="btn btn-primary" onClick={handleAdd}>
            加入
        </button>
        </div>
      </div>
    </div>
  );
}

export default FoodCard;
