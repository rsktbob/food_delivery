import { useState, useEffect } from "react"
import { fetchRestaurants, fetchFoodCategory, fetchRestaurantsByCategory } from "../../api";
import RestaurantItem from "../../components/RestaurantItem";
import FoodCategoryBar from "../../components/FoodCategoryBar";
import RestaurantSearchBar from "../../components/RestaurantSearchBar";

function CustomerHomePage({user}){
    const [restaurants, setRestaurants] = useState([]);
    const [foodCategories, setFoodCategories] = useState([]);

    useEffect(() => {
        fetchRestaurants()
        .then(data => {
            console.log(data);
            setRestaurants(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })

        fetchFoodCategory()
        .then(data => {
            console.log(data);
            setFoodCategories(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })
    }, []);

    const handleFoodCategoryClick = async (food_category) => {
        fetchRestaurantsByCategory(food_category)
        .then(data => {
            console.log(data);
            setRestaurants(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })
    }
    

    return(
        <div>
            {/* 搜尋列和分類列排成一行，使用 Bootstrap 的 row 與 col */}
            <div className="row mb-3">
                <div className="col d-flex justify-content-center">
                    <div style={{ maxWidth: '800px', width: '100%' }}>
                        <RestaurantSearchBar onSearch={setRestaurants} />
                    </div>
                </div>
            </div>

            <div className="row mb-3">
                <div className="col">
                    <FoodCategoryBar foodCategories={foodCategories} onCategoryClick={handleFoodCategoryClick}/>
                </div>
            </div>

            <hr className="my-4" style={{ borderTop: "2px solid #333" }} />

            {/* 顯示菜單項目 */}
            <div className="mt-4">
                {restaurants.length === 0 ? (
                <p>暫無餐廳</p>
                ) : (
                <div className="row">
                    {restaurants.map((item) => (
                    <div key={item.id} className="col-md-4 mb-3">
                        <RestaurantItem restaurant={item} />
                    </div>
                    ))}
                </div>
                )}
            </div>
        </div>
    )
}

export default CustomerHomePage