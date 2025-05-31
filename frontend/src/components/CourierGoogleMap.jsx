
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { 
  GoogleMap, 
  useLoadScript, 
  Marker,
  DirectionsService,
  DirectionsRenderer
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
  isNavigating = false,
  navigationStep = 0,
  onNavigationStart,
  onNavigationEnd,  
  onNavigationStepChange,
  initialPosition = { lat: 25.0330, lng: 121.5654 },
  googleMapsApiKey = "AIzaSyB4RnmMJPv2WUBk3uuGjCFW3CQWYp_zJ1A"
}) {
  const mapRef = useRef(null);
  const [deliveryPosition, setDeliveryPosition] = useState(initialPosition);
  const [directions, setDirections] = useState(null);
  const [activeRoute, setActiveRoute] = useState(null);
  
  const movementSpeed = 0.0001;
  
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: googleMapsApiKey,
    libraries: libraries
  });

  // WASD 控制外送員移動
  const handleKeyDown = useCallback((event) => {
    setDeliveryPosition(prevPosition => {
      let newPosition = { ...prevPosition };

      switch (event.key.toLowerCase()) {
        case "w":
        case "arrowup":
          newPosition.lat += movementSpeed;
          break;
        case "s":
        case "arrowdown":
          newPosition.lat -= movementSpeed;
          break;
        case "a":
        case "arrowleft":
          newPosition.lng -= movementSpeed;
          break;
        case "d":
        case "arrowright":
          newPosition.lng += movementSpeed;
          break;
        default:
          return prevPosition;
      }

      return newPosition;
    });
  }, []);

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  // 處理導航 API 回調
  const directionsCallback = useCallback((result, status) => {
    if (status === 'OK') {
      setDirections(result);
    }
    setActiveRoute(null);
  }, []);

  // 請求新路線
  const requestRoute = useCallback((origin, destination) => {
    setActiveRoute({ origin, destination });
  }, []);

  // 清除路線
  const clearRoute = useCallback(() => {
    setDirections(null);
    setActiveRoute(null);
  }, []);

  // 檢查是否到達目的地
  const checkArrival = useCallback((targetPosition) => {
    const distance = Math.sqrt(
      Math.pow(deliveryPosition.lat - targetPosition.lat, 2) + 
      Math.pow(deliveryPosition.lng - targetPosition.lng, 2)
    );
    return distance < 0.0008;
  }, [deliveryPosition]);

  // 主要導航邏輯
  useEffect(() => {
    if (!isNavigating || !selectedOrder) {
      clearRoute();
      return;
    }

    // 開始導航到餐廳
    if (navigationStep === 0) {
      requestRoute(deliveryPosition, selectedOrder.restaurant_position);
      onNavigationStepChange && onNavigationStepChange(1);
      onNavigationStart && onNavigationStart('restaurant', selectedOrder.restaurant);
    }
  }, [isNavigating, selectedOrder, navigationStep]);

  // 檢查到達目的地
  useEffect(() => {
    if (!isNavigating || !selectedOrder || navigationStep === 0) return;

    const checkTimer = setInterval(() => {
      CourierUpdatePos(user.id,deliveryPosition.lat,deliveryPosition.lng)//傳座標給後端
      console.log("transs~")
      if (navigationStep === 2) {
        // 到達餐廳，前往顧客
        clearRoute();
        setTimeout(() => {
          requestRoute(deliveryPosition, selectedOrder.customer_position);
          onNavigationStepChange && onNavigationStepChange(3);
          onNavigationStart && onNavigationStart('customer', selectedOrder.customer_name);
        }, 100);
        
      } else if (navigationStep === 4 ) {
        // 到達顧客，完成配送
        clearRoute();
        onNavigationEnd && onNavigationEnd(selectedOrder);
        onNavigationStepChange && onNavigationStepChange(0);
      }
    }, 500);

    return () => clearInterval(checkTimer);
  }, [deliveryPosition, navigationStep, isNavigating, selectedOrder, checkArrival, requestRoute, clearRoute, onNavigationStart, onNavigationEnd, onNavigationStepChange]);

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
      <Marker
        position={deliveryPosition}
        icon={{
          url: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%234ade80' stroke='white' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cpath d='M8 12l2 2 4-4'/%3E%3C/svg%3E",
          scaledSize: { width: 40, height: 40 },
          anchor: { x: 20, y: 20 }
        }}
        title="外送員 (WASD控制)"
        zIndex={1000}
      />

      {/* 餐廳標記 */}
      {selectedOrder?.restaurant && (
        <Marker
          position={selectedOrder.restaurant_position}
          icon={{
            url: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%23f59e0b' stroke='white' stroke-width='2'%3E%3Ccircle cx='12' cy='8' r='7'/%3E%3Cpath d='M8.21 13.89L7 23l5-3 5 3-1.21-9.12'/%3E%3C/svg%3E",
            scaledSize: { width: 36, height: 36 },
            anchor: { x: 18, y: 36 }
          }}
          title={selectedOrder.restaurant.name}
        />
      )}

      {/* 顧客標記 */}
      {selectedOrder?.customer_name && (
        <Marker
          position={selectedOrder.customer_position}
          icon={{
            url: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='%232563eb' stroke='white' stroke-width='2'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E",
            scaledSize: { width: 36, height: 36 },
            anchor: { x: 18, y: 36 }
          }}
          title={selectedOrder.customer_name}
        />
      )}
      
      {/* 導航服務 */}
      {activeRoute && (
        <DirectionsService
          options={{
            destination: activeRoute.destination,
            origin: activeRoute.origin,
            travelMode: 'DRIVING'
          }}
          callback={directionsCallback}
        />
      )}

      {/* 導航路線 */}
      {directions && (
        <DirectionsRenderer
          options={{
            directions: directions,
            suppressMarkers: true,
            preserveViewport: true,
            polylineOptions: {
              strokeColor: navigationStep === 1 ? '#f59e0b' : '#2563eb',
              strokeWeight: 4,
              strokeOpacity: 0.8
            }
          }}
        />
      )}
    </GoogleMap>
  );
}

export default DeliveryMap;