function FoodCategoryCard({ foodItem }) {
  return (
    <div style={{ width: 100, textAlign: "center", fontFamily: "Arial, sans-serif" }}>
      {foodItem.image && (
        <img
          src={foodItem.image}
          alt={foodItem.name}
          style={{
            width: 100,
            height: 100,
            objectFit: "cover",
            borderRadius: 8,
            marginBottom: 8,
          }}
        />
      )}
      <p style={{ margin: 0, fontSize: 14, color: "#555" }}>
        {foodItem.category?.name || "未分類"}
      </p>
    </div>
  );
}

export default FoodCategoryCard;