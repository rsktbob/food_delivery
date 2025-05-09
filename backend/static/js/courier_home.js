// courier_dashboard.js

// Mock data for testing
const mockData = {
    courier: {
        id: 1,
        name: "Alex Johnson",
        earnings_today: 45.50,
        deliveries_today: 3,
        status: "online"
    },
    active_order: null, // Will be set when an order is accepted
    available_orders: [
        {
            id: 101,
            restaurant: {
                id: 3,
                name: "Burger Palace",
                address: "123 Main St"
            },
            customer: {
                name: "Sarah Wilson",
                address: "456 Oak Ave, Apt 7B"
            },
            status: "Accepted",
            total_price: 27.95,
            delivery_fee: 4.99,
            payment_method: "Credit Card",
            created_at: "2025-05-01T10:30:00",
            items: [
                { name: "Deluxe Burger", quantity: 2, price: 9.99 },
                { name: "French Fries", quantity: 1, price: 3.99 },
                { name: "Chocolate Shake", quantity: 1, price: 3.99 }
            ]
        },
        {
            id: 102,
            restaurant: {
                id: 7,
                name: "Pizza Heaven",
                address: "789 Elm St"
            },
            customer: {
                name: "Michael Lee",
                address: "222 Pine Rd"
            },
            status: "Accepted",
            total_price: 34.50,
            delivery_fee: 3.99,
            payment_method: "Cash on Delivery",
            created_at: "2025-05-01T10:35:00",
            items: [
                { name: "Large Pepperoni Pizza", quantity: 1, price: 18.99 },
                { name: "Garlic Knots", quantity: 1, price: 5.99 },
                { name: "2L Soda", quantity: 1, price: 3.99 }
            ]
        },
        {
            id: 103,
            restaurant: {
                id: 12,
                name: "Taco Fiesta",
                address: "333 Maple Ave"
            },
            customer: {
                name: "Emma Garcia",
                address: "555 Walnut St, Unit 12"
            },
            status: "Accepted",
            total_price: 22.75,
            delivery_fee: 4.50,
            payment_method: "Credit Card",
            created_at: "2025-05-01T10:40:00",
            items: [
                { name: "Taco Combo", quantity: 1, price: 12.99 },
                { name: "Nachos", quantity: 1, price: 7.99 },
                { name: "Mexican Soda", quantity: 1, price: 1.99 }
            ]
        }
    ],
    order_history: [
        {
            id: 98,
            restaurant: {
                name: "Sushi Express",
                address: "444 Cherry Ln"
            },
            customer: {
                name: "David Kim",
                address: "777 Spruce Ct"
            },
            status: "Finish",
            total_price: 39.95,
            delivery_fee: 5.99,
            payment_method: "Credit Card",
            created_at: "2025-05-01T08:15:00",
            delivered_at: "2025-05-01T09:05:00"
        },
        {
            id: 97,
            restaurant: {
                name: "Thai Delight",
                address: "888 Willow Dr"
            },
            customer: {
                name: "Jennifer Smith",
                address: "999 Cedar Blvd"
            },
            status: "Finish",
            total_price: 28.50,
            delivery_fee: 4.50,
            payment_method: "Credit Card",
            created_at: "2025-05-01T07:20:00",
            delivered_at: "2025-05-01T08:10:00"
        },
        {
            id: 95,
            restaurant: {
                name: "Panda Express",
                address: "111 Bamboo St"
            },
            customer: {
                name: "Robert Johnson",
                address: "222 Palm Ave"
            },
            status: "Finish",
            total_price: 24.75,
            delivery_fee: 3.99,
            payment_method: "Cash on Delivery",
            created_at: "2025-04-30T18:30:00",
            delivered_at: "2025-04-30T19:15:00"
        }
    ]
};

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    updateCourierInfo();
    renderAvailableOrders();
    renderOrderHistory();
    
    // Set up event listeners
    setupTabNavigation();
    setupOrderActions();
    setupStatusToggle();
});

function updateCourierInfo() {
    document.getElementById('earnings-today').textContent = `$${mockData.courier.earnings_today.toFixed(2)}`;
    document.getElementById('deliveries-today').textContent = mockData.courier.deliveries_today;
    
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    if (mockData.courier.status === 'online') {
        statusIndicator.className = 'status-online';
        statusText.textContent = 'Online';
    } else {
        statusIndicator.className = 'status-offline';
        statusText.textContent = 'Offline';
    }
    
    document.getElementById('active-delivery').textContent = mockData.active_order ? 'Active' : 'None';
}

function renderAvailableOrders() {
    const ordersContainer = document.getElementById('available-orders');
    
    if (mockData.courier.status === 'offline') {
        ordersContainer.innerHTML = `<div class="empty-state">You are currently offline. Go online to see available orders.</div>`;
        return;
    }
    
    if (mockData.active_order) {
        ordersContainer.innerHTML = `<div class="empty-state">You have an active order. Finish it before accepting new orders.</div>`;
        return;
    }
    
    if (mockData.available_orders.length === 0) {
        ordersContainer.innerHTML = `<div class="empty-state">No orders available at the moment. Check back soon!</div>`;
        return;
    }
    
    let ordersHTML = '';
    
    mockData.available_orders.forEach(order => {
        ordersHTML += `
            <div class="order-card" data-order-id="${order.id}">
                <div class="order-header">
                    <span class="order-id">Order #${order.id}</span>
                    <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
                </div>
                <div class="order-info">
                    <div class="info-row">
                        <span class="info-label">Restaurant:</span>
                        <span class="info-value">${order.restaurant.name}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Location:</span>
                        <span class="info-value">${order.restaurant.address}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Delivery to:</span>
                        <span class="info-value">${order.customer.address}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Items:</span>
                        <span class="info-value">${order.items.length} items</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Payment:</span>
                        <span class="info-value">${order.payment_method}</span>
                    </div>
                </div>
                <div class="order-footer">
                    <div class="order-price">$${(order.total_price + order.delivery_fee).toFixed(2)}</div>
                    <button class="order-action-btn accept-order-btn" data-order-id="${order.id}">Accept Order</button>
                </div>
            </div>
        `;
    });
    
    ordersContainer.innerHTML = ordersHTML;
    
    // Add event listeners to accept buttons
    document.querySelectorAll('.accept-order-btn').forEach(button => {
        button.addEventListener('click', function() {
            const orderId = parseInt(this.getAttribute('data-order-id'));
            acceptOrder(orderId);
        });
    });
}

function renderActiveOrder() {
    const activeOrderContainer = document.getElementById('active-order-details');
    const pickupBtn = document.getElementById('pickup-btn');
    const deliveredBtn = document.getElementById('delivered-btn');
    
    if (!mockData.active_order) {
        activeOrderContainer.innerHTML = `<div class="empty-state">No active order</div>`;
        pickupBtn.disabled = true;
        deliveredBtn.disabled = true;
        return;
    }
    
    const order = mockData.active_order;
    
    let itemsHTML = '';
    order.items.forEach(item => {
        itemsHTML += `
            <div class="order-item">
                <span class="item-quantity">${item.quantity}x</span>
                <span class="item-name">${item.name}</span>
                <span class="item-price">$${(item.price * item.quantity).toFixed(2)}</span>
            </div>
        `;
    });
    
    activeOrderContainer.innerHTML = `
        <div class="order-card active">
            <div class="order-header">
                <span class="order-id">Order #${order.id}</span>
                <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
            </div>
            <div class="order-info">
                <div class="info-row">
                    <span class="info-label">Restaurant:</span>
                    <span class="info-value">${order.restaurant.name}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Pickup from:</span>
                    <span class="info-value">${order.restaurant.address}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Customer:</span>
                    <span class="info-value">${order.customer.name}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Deliver to:</span>
                    <span class="info-value">${order.customer.address}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Payment:</span>
                    <span class="info-value">${order.payment_method}</span>
                </div>
            </div>
            <div class="order-items">
                <h4>Order Items</h4>
                ${itemsHTML}
            </div>
            <div class="order-summary">
                <div class="summary-row">
                    <span>Subtotal:</span>
                    <span>$${order.total_price.toFixed(2)}</span>
                </div>
                <div class="summary-row">
                    <span>Delivery Fee:</span>
                    <span>$${order.delivery_fee.toFixed(2)}</span>
                </div>
                <div class="summary-row total">
                    <span>Total:</span>
                    <span>$${(order.total_price + order.delivery_fee).toFixed(2)}</span>
                </div>
            </div>
        </div>
    `;
    
    // Update action buttons based on order status
    if (order.status === 'Assigned') {
        pickupBtn.disabled = false;
        deliveredBtn.disabled = true;
    } else if (order.status === 'Picked_Up') {
        pickupBtn.disabled = true;
        deliveredBtn.disabled = false;
    } else {
        pickupBtn.disabled = true;
        deliveredBtn.disabled = true;
    }
}

function renderOrderHistory() {
    const historyContainer = document.getElementById('history-orders');
    
    if (mockData.order_history.length === 0) {
        historyContainer.innerHTML = `<div class="empty-state">No delivery history yet</div>`;
        return;
    }
    
    let historyHTML = '';
    
    mockData.order_history.forEach(order => {
        historyHTML += `
            <div class="order-card">
                <div class="order-header">
                    <span class="order-id">Order #${order.id}</span>
                    <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
                </div>
                <div class="order-info">
                    <div class="info-row">
                        <span class="info-label">Restaurant:</span>
                        <span class="info-value">${order.restaurant.name}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Customer:</span>
                        <span class="info-value">${order.customer.name}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Delivered to:</span>
                        <span class="info-value">${order.customer.address}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Completed:</span>
                        <span class="info-value">${formatDate(order.delivered_at)}</span>
                    </div>
                </div>
                <div class="order-footer">
                    <div class="order-price">$${(order.total_price + order.delivery_fee).toFixed(2)}</div>
                    <span class="earning-label">Your earning: $${(order.delivery_fee * 0.8).toFixed(2)}</span>
                </div>
            </div>
        `;
    });
    
    historyContainer.innerHTML = historyHTML;
}

function acceptOrder(orderId) {
    // Find the order in available orders
    const orderIndex = mockData.available_orders.findIndex(order => order.id === orderId);
    
    if (orderIndex === -1) return;
    
    // Get the order and update its status
    const order = mockData.available_orders[orderIndex];
    order.status = 'Assigned';
    
    // Set as active order and remove from available
    mockData.active_order = order;
    mockData.available_orders.splice(orderIndex, 1);
    
    // Update UI
    updateCourierInfo();
    renderAvailableOrders();
    renderActiveOrder();
    
    // Switch to active tab
    switchTab('active');
    
    // Simulate API call
    console.log(`Order #${orderId} accepted by courier`);
    
    // In real app, you would make an API call here:
    /*
    fetch('/api/courier/accept-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            order_id: orderId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Order accepted successfully');
        } else {
            console.error('Failed to accept order:', data.message);
        }
    })
    .catch(error => {
        console.error('Error accepting order:', error);
    });
    */
}

function markOrderAsPickedUp() {
    if (!mockData.active_order) return;
    
    // Update order status
    mockData.active_order.status = 'Picked_Up';
    
    // Update UI
    renderActiveOrder();
    
    // Simulate API call
    console.log(`Order #${mockData.active_order.id} marked as picked up`);
    
    // In real app, you would make an API call here
}

function markOrderAsDelivered() {
    if (!mockData.active_order) return;
    
    // Update order status
    mockData.active_order.status = 'Finish';
    
    // Add to order history
    mockData.active_order.delivered_at = new Date().toISOString();
    mockData.order_history.unshift(mockData.active_order);
    
    // Update courier stats
    mockData.courier.deliveries_today += 1;
    mockData.courier.earnings_today += mockData.active_order.delivery_fee * 0.8; // 80% of delivery fee
    
    // Clear active order
    mockData.active_order = null;
    
    // Update UI
    updateCourierInfo();
    renderActiveOrder();
    renderOrderHistory();
    renderAvailableOrders();
    
    // Simulate API call
    console.log(`Order delivered successfully`);
    
    // Switch to available tab after a short delay
    setTimeout(() => {
        switchTab('available');
    }, 1500);
    
    // In real app, you would make an API call here
}

function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update active button
    document.querySelectorAll('.tab-button').forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    // Update active content
    document.querySelectorAll('.tab-content').forEach(content => {
        if (content.id === `${tabName}-tab`) {
            content.classList.add('active');
        } else {
            content.classList.remove('active');
        }
    });
}

function setupOrderActions() {
    // Pickup button
    document.getElementById('pickup-btn').addEventListener('click', function() {
        markOrderAsPickedUp();
    });
    
    // Delivered button
    document.getElementById('delivered-btn').addEventListener('click', function() {
        markOrderAsDelivered();
    });
}

function setupStatusToggle() {
    const statusIndicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');
    
    document.querySelector('.courier-status').addEventListener('click', function() {
        if (mockData.active_order) {
            alert('You cannot go offline while you have an active order.');
            return;
        }
        
        if (mockData.courier.status === 'online') {
            mockData.courier.status = 'offline';
            statusIndicator.className = 'status-offline';
            statusText.textContent = 'Offline';
        } else {
            mockData.courier.status = 'online';
            statusIndicator.className = 'status-online';
            statusText.textContent = 'Online';
        }
        
        renderAvailableOrders();
    });
}

// Helpers
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true
    });
}

// Function to get CSRF token (for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}