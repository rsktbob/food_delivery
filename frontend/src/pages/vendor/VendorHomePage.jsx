import RestaurantInfo from "../../components/RestaurantInfo"
import { useState, useEffect } from "react"
import {fetchRestaurantInfo} from "../../api";

function VendorHomePage({user}){
    const [restaurantInfo, setRestaurantInfo] = useState({
        name: '',
        address: '',
        image_url: '',
    });

    useEffect(() => {
        fetchRestaurantInfo()
        .then(data => {
            console.log(data);
            setRestaurantInfo(data);
        })
        .catch(error => {
            console.log(`error: ${error}`);
        })
    }, []);

    return(
    <div className="container py-5">
      <h2 className="display-4">歡迎回來，{user.name}！</h2>

      <RestaurantInfo name={restaurantInfo.name} address={restaurantInfo.address} image_url={restaurantInfo.image}/>
      <section className="row mt-5">

      </section>
    </div>
    )
}

export default VendorHomePage