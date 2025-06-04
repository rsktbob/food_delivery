function FoodCategoryCard({ foodCategory, onClick }) {
  return (
    <a
      className="text-center"
      style={{
        width: 100,
        fontFamily: "Arial, sans-serif",
        flexShrink: 0,
        textDecoration: "none", // 移除底線
        cursor: "pointer",      // 顯示點擊樣式
        color: "inherit",       // 保持文字顏色
        display: "inline-block" // 保持區塊樣式
      }}
      onClick={onClick}
    >
      {foodCategory.image && (
        <img
          src={foodCategory.image}
          alt={foodCategory.name}
          className="mb-2"
          style={{
            width: 60,
            height: 60,
            objectFit: "cover",
            borderRadius: 8,
          }}
        />
      )}
      <p className="mb-0" style={{ fontSize: 14, color: "#555" }}>
        {foodCategory.name || "未分類"}
      </p>
    </a>
  );
}

export default FoodCategoryCard;