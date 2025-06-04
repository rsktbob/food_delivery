import React, { useState } from "react";
import { fetchRestaurantsByName } from "../api";

function RestaurantSearchBar({ onSearch }) {
  const [keyword, setKeyword] = useState("");

  const handleInputChange = (e) => {
    setKeyword(e.target.value);
  };

  const handleSearch = () => {
    if (!keyword.trim()) return;
    fetchRestaurantsByName(keyword.trim())
      .then(data => onSearch(data))
      .catch(err => console.error(err));
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="input-group mb-3" style={{ maxWidth: 700 }}>
      <input
        type="text"
        className="form-control"
        placeholder="輸入餐廳名稱或關鍵字搜尋"
        value={keyword}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
      />
      <button className="btn btn-primary" onClick={handleSearch}>
        搜尋
      </button>
    </div>
  );
}

export default RestaurantSearchBar;
