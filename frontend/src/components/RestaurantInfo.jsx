import React from 'react';

function RestaurantInfo({ restaurant }) {
  return (
    <div className="w-100 h-100 bg-white">
      <div className="card-body p-4">
        <h3 className="card-title h4 mb-4 pb-2 border-bottom d-flex align-items-center">
          <span className="me-2">🍽️</span>
          餐廳資訊
        </h3>

        {/* 餐廳基本資訊 */}
        <div className="row g-3 mb-4">
          <div className="col-md-6">
            <div className="d-flex align-items-start mb-3">
              <div className="bg-primary bg-opacity-10 rounded-circle p-2 me-3 flex-shrink-0">
                <span className="text-primary fw-bold">名</span>
              </div>
              <div>
                <strong className="text-dark">名稱：</strong>
                <span className="text-muted ms-1">{restaurant.name || '未提供'}</span>
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="d-flex align-items-start mb-3">
              <div className="bg-success bg-opacity-10 rounded-circle p-2 me-3 flex-shrink-0">
                <span className="text-success fw-bold">類</span>
              </div>
              <div>
                <strong className="text-dark">類型：</strong>
                <span className="text-muted ms-1">{restaurant.category || '未提供'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="row g-3 mb-4">
          <div className="col-12">
            <div className="d-flex align-items-start mb-3">
              <div className="bg-danger bg-opacity-10 rounded-circle p-2 me-3 flex-shrink-0">
                <span className="text-danger">📍</span>
              </div>
              <div>
                <strong className="text-dark">地址：</strong>
                <span className="text-muted ms-1">{restaurant.address || '未提供'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="row g-3 mb-4">
          <div className="col-md-6">
            <div className="d-flex align-items-start mb-3">
              <div className="bg-info bg-opacity-10 rounded-circle p-2 me-3 flex-shrink-0">
                <span className="text-info">📞</span>
              </div>
              <div>
                <strong className="text-dark">電話：</strong>
                <span className="text-muted ms-1 font-monospace">{restaurant.phone_number || '未提供'}</span>
              </div>
            </div>
          </div>

          <div className="col-md-6">
            <div className="d-flex align-items-start mb-3">
              <div className="bg-warning bg-opacity-10 rounded-circle p-2 me-3 flex-shrink-0">
                <span className="text-warning">🕒</span>
              </div>
              <div>
                <strong className="text-dark">營業時間：</strong>
                <span className="text-muted ms-1">{restaurant.hours || '未提供'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* 餐廳圖片 */}
        {restaurant.image ? (
          <div className="text-center mb-4">
            <img
              src={restaurant.image}
              alt="餐廳圖片"
              className="img-fluid rounded shadow-sm"
              style={{ maxWidth: '100%', maxHeight: '360px', objectFit: 'cover' }}
            />
          </div>
        ) : (
          <div className="text-center mb-4">
            <div className="bg-light rounded p-5 d-inline-block">
              <div className="text-muted">
                <div style={{ fontSize: '3rem' }} className="mb-2">🏪</div>
                <span>未提供餐廳圖片</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RestaurantInfo;
