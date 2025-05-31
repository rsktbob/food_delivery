import RestaurantInfo from "../../components/RestaurantInfo"
import { useState, useEffect } from "react"
import {fetchRestaurant} from "../../api";

function VendorHomePage({user}){
    const [restaurant, setRestaurant] = useState({
        name: '',
        address: '',
        image: '',
    });

    useEffect(() => {
        fetchRestaurant(user.restaurant_id)
        .then(data => {
            setRestaurant(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })
    }, []);

    return(
    <div className="container py-5">
      <h2 className="display-4">歡迎回來，{user.name}！</h2>

      <RestaurantInfo restaurant={restaurant}/>
      <section className="row mt-5">
      </section>
    </div>
    )
}

export default VendorHomePage