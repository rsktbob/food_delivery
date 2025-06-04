import FoodCategoryCard from "./FoodCategoryCard";

function FoodCategoryBar({ foodCategories = [], onCategoryClick }) {
  return (
    <div className="w-100">
      <div className="overflow-auto">
        <div
          className="d-flex flex-row px-3"
          style={{ gap: "1rem", minWidth: "max-content" }}
        >
          {foodCategories.map((foodCategory, index) => (
            <div
              key={foodCategory.id || index}
              className="cursor-pointer"
              onClick={() => onCategoryClick(foodCategory.name)}
              style={{ flex: "0 0 auto" }}
            >
              <FoodCategoryCard foodCategory={foodCategory} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default FoodCategoryBar;