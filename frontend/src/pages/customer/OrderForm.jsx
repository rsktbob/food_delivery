import React, { useState, useEffect } from 'react';
import { fetchCartItems, createOrders } from '../../api'
import { useJsApiLoader } from '@react-google-maps/api';
import { useNavigate } from 'react-router-dom';

export default function OrderForm({user}) {
  const [address, setAddress] = useState(user.address);
  const [payment, setPayment] = useState(null);
  const [cartItems, setCartItems] = useState([]);

  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: 'AIzaSyCgoPkIvc9J-vnVbVDyYDztNTZngKPecEE' // 替換成你的 API Key
  });

  const geocodeAddress = async (address) => {
    if (!isLoaded) {
      throw new Error('Google Maps API 尚未載入');
    }

    return new Promise((resolve, reject) => {
      const geocoder = new window.google.maps.Geocoder();
      
      geocoder.geocode({ address: address }, (results, status) => {
        if (status === 'OK' && results[0]) {
          const location = results[0].geometry.location;
          resolve({
            lat: location.lat(),
            lng: location.lng()
          });
        } else {
          reject(new Error('地址轉換失敗'));
        }
      });
    });
  };

  const navigate = useNavigate();
  const handleSubmit = async () => {
    if (!address || !payment) {
      alert('請填寫完整資訊');
      return;
    }

    try {
      const coordinates = await geocodeAddress(address);
      const latitude = coordinates.lat;
      const longitude = coordinates.lng;
      await createOrders(latitude, longitude, address, payment);
      alert('訂單建立成功！');
      navigate(`/map`);
    } catch (error) {
      alert('地址錯誤，請重新舔血');
      return;
    }
  };

  useEffect(() => {
    fetchCartItems()
      .then(data => {
        setCartItems(data);
        console.log(data);
      })
      .catch(error => {
        console.error(`error: ${error}`);
      });
  },[])

  return (
    <div className="container mt-4">
      <div className="card">
        <div className="card-header">
          <h4>確認訂單</h4>
        </div>
        <div className="card-body">
          <div className="mb-3">
            <label className="form-label"><strong>外送地址</strong></label>
            <input 
              type="text" 
              className="form-control" 
              placeholder="請輸入外送地址"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
            />
          </div>
          
          <div className="mb-3">
            <label className="form-label"><strong>付款方式</strong></label>
            <input 
              type="text" 
              className="form-control" 
              placeholder="請輸入付款方式"
              value={payment}
              onChange={(e) => setPayment(e.target.value)}
            />
          </div>

          <div className="mb-4">
            <label className="form-label"><strong>品項</strong></label>
            {cartItems.map(item => (
              <div key={item.id}>{item.foodItem.name} x {item.quantity}</div>
            ))}
          </div>

          <div className="mb-4">
            <label className="form-label"><strong>總金額</strong></label>
            <div className="fs-5 text-primary">NT$ 350</div>
          </div>
          
          <div className="d-grid">
            <button className="btn btn-primary btn-lg" onClick={handleSubmit}>
              確認下單
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}