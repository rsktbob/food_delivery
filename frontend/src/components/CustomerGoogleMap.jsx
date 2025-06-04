import React, { useState, useEffect, useRef } from 'react';
import { 
  GoogleMap, 
  useLoadScript, 
  Marker
} from '@react-google-maps/api';
import { CourierUpdatePos } from '../api';

const mapContainerStyle = {
  width: '100%',
  height: '85vh'
};

const libraries = ["places"];

function DeliveryMap({ 
  user,
  selectedOrder = null,
  initialPosition = { lat: 25.0330, lng: 121.5654 },
  googleMapsApiKey = "AIzaSyCgoPkIvc9J-vnVbVDyYDztNTZngKPecEE"
}) {
  const mapRef = useRef(null);
  const [deliveryPosition, setDeliveryPosition] = useState(initialPosition);
  
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: googleMapsApiKey,
    libraries: libraries
  });

  useEffect(() => {
    console.log("Order updated:", selectedOrder);
  }, [selectedOrder]);
  if (loadError) return <div style={{padding: '20px', color: 'red'}}>地圖載入失敗</div>;
  if (!isLoaded) return <div style={{padding: '20px'}}>地圖載入中...</div>;

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      center={deliveryPosition}
      zoom={16}
      onLoad={(map) => mapRef.current = map}
      options={{
        disableDefaultUI: true,
        zoomControl: true,
        gestureHandling: 'greedy'
      }}
    >
      {/* 外送員標記 */}
      {selectedOrder?.courier && (
        <Marker
          position={{lat: selectedOrder.courier.latitude, lng: selectedOrder.courier.longitude}}
          icon={{
            url: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%234ade80' stroke='white' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M8 12l2 2 4-4'/%3E%3C/svg%3E",
            scaledSize: { width: 40, height: 40 },
            anchor: { x: 20, y: 20 }
          }}
          title="外送員"
          zIndex={1000}
        />
      )}

      {/* 餐廳標記 */}
      {selectedOrder?.restaurant && (
        <Marker
          position={{lat: selectedOrder.restaurant.latitude, lng: selectedOrder.restaurant.longitude}}
          icon={{
            url: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%23f59e0b' stroke='white' stroke-width='2'%3E%3Ccircle cx='12' cy='8' r='7'/%3E%3Cpath d='M8.21 13.89L7 23l5-3 5 3-1.21-9.12'/%3E%3C/svg%3E",
            scaledSize: { width: 36, height: 36 },
            anchor: { x: 18, y: 36 }
          }}
          title={selectedOrder.restaurant.name}
        />
      )}

      {/* 顧客標記 */}
      {selectedOrder && (
        <Marker
          position={{lat: selectedOrder.latitude, lng: selectedOrder.longitude}}
          icon={{
            url: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%232563eb' stroke='white' stroke-width='2'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E",
            scaledSize: { width: 36, height: 36 },
            anchor: { x: 18, y: 36 }
          }}
          title={selectedOrder.customer_name}
        />
      )}
    </GoogleMap>
  );
}

export default DeliveryMap;