function CartItem({ cartItem, onQuantityChange, onRemove }) {
  const handleQuantityChange = (e) => {
    const val = parseInt(e.target.value);
    if (!isNaN(val) && val >= 1) {
      onQuantityChange(cartItem.id, val);
    }
  };

  return (
    <div className="cart-item d-flex align-items-center border-bottom py-3">
      {cartItem.foodItem.image && (
        <img
          src={cartItem.foodItem.image}
          alt={cartItem.foodItem.name}
          style={{ width: "80px", height: "80px", objectFit: "cover", borderRadius: "8px" }}
          className="me-3"
        />
      )}
      <div className="flex-grow-1">
        <h6>{cartItem.name}</h6>
        <p className="mb-1">單價：${cartItem.foodItem.price}</p>
        <p className="mb-1">小計：${(cartItem.foodItem.price * cartItem.quantity).toFixed(2)}</p>
      </div>
      <div className="d-flex align-items-center">
        <input
          type="number"
          min="1"
          value={cartItem.quantity}
          onChange={handleQuantityChange}
          className="form-control me-3"
          style={{ width: "70px" }}
        />
        <button className="btn btn-danger" onClick={() => onRemove(cartItem.id)}>
          刪除
        </button>
      </div>
    </div>
  );
}

export default CartItem;