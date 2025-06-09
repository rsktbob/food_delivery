function MenuItem({ food, onDelete, onEdit }) {
  return (
    <div className="card">
      {food.name && (
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
        <div className="d-flex justify-content-between">
          <button
            className="btn btn-warning"
            onClick={() => { onEdit(food.id, food) }}
          >
            編輯
          </button>
          <button
            className="btn btn-danger"
            onClick={() => onDelete(food.id)}
          >
            刪除
          </button>
        </div>
      </div>
    </div>
  );
}

export default MenuItem;