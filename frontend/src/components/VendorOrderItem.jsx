import React from 'react';

function VendorOrderItem({ order, onAccept, onReject }) {
    return (
        <div className={`list-group-item ${order.status === 'accepted' ? 'list-group-item list-group-item-success' : 'list-group-item'}`}>
            <div className="d-flex flex-column">
                <div className="mb-1">
                    <strong>訂單編號:</strong> {order.id}
                </div>

                <ul className="mt-2 ps-3">
                    {order.items && order.items.map((item, index) => (
                        <li key={index}>
                            {item.food_name} x {item.quantity}（總價 ${item.total_price}）
                        </li>
                    ))}
                </ul>

                {/* 按鈕區 */}
                <div className="mt-3">
                    {order.status !== 'accepted' && (
                        <>
                            <button
                                className="btn btn-success me-2"
                                onClick={() => onAccept(order.id)}
                            >
                                接受
                            </button>
                            <button
                                className="btn btn-danger"
                                onClick={() => onReject(order.id)}
                            >
                                拒絕
                            </button>
                        </>
                    )
                    }
                </div>
            </div>
        </div>
    );
}

export default VendorOrderItem;