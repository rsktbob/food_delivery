function RestaurantInfo({ name, address, image_url}) {
  return (
    <div className="card mt-4 p-4 shadow">
      <h3 className="h5 font-weight-bold">餐廳資訊</h3>
      <p><strong>名稱：</strong>{name}</p>
      <p><strong>地址：</strong>{address}</p>
      <img src={image_url} alt="未有餐廳圖片" style={{width: '300px'}} />
    </div>
  );
}

export default RestaurantInfo