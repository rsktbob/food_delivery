document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const ordersList = document.getElementById('orders-list');
    const refreshButton = document.getElementById('refresh-orders');
    const tabButtons = document.querySelectorAll('.tab-button');
    const modal = document.getElementById('order-detail-modal');
    const closeModal = document.querySelector('.close-modal');
    const acceptOrderBtn = document.getElementById('accept-order-btn');
    const rejectOrderBtn = document.getElementById('reject-order-btn');
    const orderDetailContent = document.querySelector('.order-detail-content');
    const toast = document.getElementById('toast-notification');
    const toastMessage = document.getElementById('toast-message');

    // Stats counters
    const pendingCount = document.getElementById('pending-count');
    const acceptedCount = document.getElementById('accepted-count');
    const deliveryCount = document.getElementById('delivery-count');
    const completedCount = document.getElementById('completed-count');

    // State
    let currentRestaurantId = '1'; // Fake restaurant ID
    let orders = [];
    let currentFilter = 'all';
    let selectedOrderId = null;

    // Fake menu items for generating order items
    const menuItems = [
        { id: 1, name: "Spicy Chicken Burger", price: 12.99 },
        { id: 2, name: "Vegetarian Pizza", price: 15.99 },
        { id: 3, name: "Beef Noodle Soup", price: 13.50 },
        { id: 4, name: "Caesar Salad", price: 9.99 },
        { id: 5, name: "Chocolate Lava Cake", price: 7.99 },
        { id: 6, name: "Iced Latte", price: 4.99 },
        { id: 7, name: "French Fries", price: 5.99 },
        { id: 8, name: "Chicken Tenders", price: 10.99 },
        { id: 9, name: "Garlic Bread", price: 3.99 },
        { id: 10, name: "Fruit Smoothie", price: 6.99 }
    ];

    // Fake customer data
    const customers = [
        { id: 1, username: "John Smith", phone: "555-123-4567" },
        { id: 2, username: "Emma Wilson", phone: "555-234-5678" },
        { id: 3, username: "Michael Chen", phone: "555-345-6789" },
        { id: 4, username: "Sophia Rodriguez", phone: "555-456-7890" },
        { id: 5, username: "David Kim", phone: "555-567-8901" }
    ];

    // Addresses for random assignment
    const addresses = [
        "123 Main St, Apt 4B, Cityville",
        "456 Oak Avenue, Townsburg",
        "789 Pine Road, Villageton",
        "321 Maple Drive, Hamletville",
        "654 Birch Boulevard, Downtown",
        "987 Cedar Lane, Uptown",
        "741 Elm Street, Countryside",
        "852 Willow Path, Riverside",
        "963 Spruce Court, Hillside",
        "159 Redwood Way, Lakeside"
    ];

    // Payment methods
    const paymentMethods = ["Credit Card", "Cash on Delivery", "Digital Wallet", "Bank Transfer"];

    // Generate fake orders
    function generateFakeOrders(count = 15) {
        const statuses = ['Created', 'Accepted', 'Assigned', 'Picked_Up', 'Finish'];
        const orders = [];
        
        const now = new Date();
        
        for (let i = 1; i <= count; i++) {
            // Generate random date within the last 24 hours
            const orderDate = new Date(now);
            orderDate.setHours(now.getHours() - Math.random() * 24);
            
            // Select random status with weighted distribution
            // More likely to be recent statuses (Created, Accepted) than completed ones
            let status;
            const rand = Math.random();
            if (rand < 0.3) status = statuses[0]; // Created - 30%
            else if (rand < 0.6) status = statuses[1]; // Accepted - 30%
            else if (rand < 0.8) status = statuses[2]; // Assigned - 20%
            else if (rand < 0.9) status = statuses[3]; // Picked_Up - 10%
            else status = statuses[4]; // Finish - 10%
            
            // Generate random customer
            const customer = customers[Math.floor(Math.random() * customers.length)];
            
            // Generate random delivery address
            const deliveryAddress = addresses[Math.floor(Math.random() * addresses.length)];
            
            // Generate random payment method
            const paymentMethod = paymentMethods[Math.floor(Math.random() * paymentMethods.length)];
            
            // Generate random order items
            const itemCount = 1 + Math.floor(Math.random() * 5); // 1-5 items
            const items = [];
            let totalPrice = 0;
            
            for (let j = 0; j < itemCount; j++) {
                const menuItem = menuItems[Math.floor(Math.random() * menuItems.length)];
                const quantity = 1 + Math.floor(Math.random() * 3); // 1-3 quantity
                const hasInstructions = Math.random() < 0.3; // 30% chance of special instructions
                
                const specialInstructions = hasInstructions 
                    ? ["No onions please", "Extra spicy", "Gluten-free if possible", "Sauce on the side", "No ice"][Math.floor(Math.random() * 5)]
                    : "";
                
                const itemPrice = menuItem.price * quantity;
                totalPrice += itemPrice;
                
                items.push({
                    id: j + 1,
                    menu_item: menuItem,
                    quantity: quantity,
                    unit_price: menuItem.price,
                    special_instructions: specialInstructions
                });
            }
            
            // Add delivery fee
            const deliveryFee = 3.99;
            
            // Create order object
            orders.push({
                id: i,
                customer: customer,
                created_at: orderDate.toISOString(),
                updated_at: orderDate.toISOString(),
                status: status,
                delivery_address: deliveryAddress,
                payment_method: paymentMethod,
                items: items,
                total_price: totalPrice.toFixed(2),
                delivery_fee: deliveryFee.toFixed(2),
                grand_total: (totalPrice + deliveryFee).toFixed(2),
                is_paid: Math.random() < 0.7 // 70% chance of being paid
            });
        }
        
        return orders;
    }

    // Load fake data on initialization
    function initializeDashboard() {
        // Generate fake orders
        orders = generateFakeOrders(15);
        
        // Update stats and display orders
        updateStats();
        displayOrders();
        
        console.log("Dashboard initialized with fake data");
    }

    // Update dashboard statistics
    function updateStats() {
        if (!orders || orders.length === 0) {
            pendingCount.textContent = '0';
            acceptedCount.textContent = '0';
            deliveryCount.textContent = '0';
            completedCount.textContent = '0';
            return;
        }
        
        // Count orders by status
        const counts = {
            'Created': 0,
            'Accepted': 0,
            'Assigned': 0,
            'Picked_Up': 0,
            'Finish': 0
        };
        
        orders.forEach(order => {
            if (counts.hasOwnProperty(order.status)) {
                counts[order.status]++;
            }
        });
        
        // Update UI counters
        pendingCount.textContent = counts['Created'];
        acceptedCount.textContent = counts['Accepted'];
        deliveryCount.textContent = counts['Assigned'] + counts['Picked_Up'];
        completedCount.textContent = counts['Finish'];
    }

    // Display orders based on current filter
    function displayOrders() {
        if (!orders || orders.length === 0) {
            ordersList.innerHTML = `
                <div class="no-orders-message">
                    <i class="fas fa-coffee"></i>
                    <p>No orders at the moment. Take a break!</p>
                </div>
            `;
            return;
        }
        
        // Filter orders by status if needed
        const filteredOrders = currentFilter === 'all' 
            ? orders 
            : orders.filter(order => order.status === currentFilter);
        
        if (filteredOrders.length === 0) {
            ordersList.innerHTML = `
                <div class="no-orders-message">
                    <i class="fas fa-filter"></i>
                    <p>No ${currentFilter.toLowerCase()} orders found.</p>
                </div>
            `;
            return;
        }
        
        // Sort orders: Created first, then by most recent
        filteredOrders.sort((a, b) => {
            // Put 'Created' status first
            if (a.status === 'Created' && b.status !== 'Created') return -1;
            if (a.status !== 'Created' && b.status === 'Created') return 1;
            
            // Then sort by date (most recent first)
            return new Date(b.created_at) - new Date(a.created_at);
        });
        
        // Clear the list
        ordersList.innerHTML = '';
        
        // Add each order card
        filteredOrders.forEach(order => {
            const orderCard = document.createElement('div');
            orderCard.className = 'order-card';
            orderCard.dataset.orderId = order.id;
            
            // Format date for display
            const orderDate = new Date(order.created_at);
            const formattedDate = orderDate.toLocaleString();
            
            // Create order card HTML
            orderCard.innerHTML = `
                <div class="order-header">
                    <span class="order-id">Order #${order.id}</span>
                    <span class="order-time">${formattedDate}</span>
                </div>
                <div class="order-status status-${order.status.toLowerCase()}">${formatStatus(order.status)}</div>
                <div class="order-customer">
                    <i class="fas fa-user"></i> ${order.customer.username}
                </div>
                <div class="order-address">
                    <i class="fas fa-map-marker-alt"></i> ${order.delivery_address}
                </div>
                <div class="order-total">
                    Total: $${parseFloat(order.total_price).toFixed(2)}
                </div>
                <div class="order-actions">
                    ${getOrderActions(order)}
                </div>
            `;
            
            // Add click event to show order details
            orderCard.addEventListener('click', (e) => {
                // If clicking on a button inside the card, don't open the modal
                if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                    return;
                }
                
                openOrderDetails(order);
            });
            
            ordersList.appendChild(orderCard);
        });
        
        // Add event listeners to action buttons
        document.querySelectorAll('.btn-accept').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent opening the modal
                const orderId = e.target.closest('.order-card').dataset.orderId;
                acceptOrder(orderId);
            });
        });
        
        document.querySelectorAll('.btn-reject').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent opening the modal
                showToast('Order rejection feature is coming soon.');
            });
        });
    }

    // Format order status for display
    function formatStatus(status) {
        switch (status) {
            case 'Created':
                return 'Pending';
            case 'Picked_Up':
                return 'Picked Up';
            default:
                return status;
        }
    }

    // Get appropriate action buttons based on order status
    function getOrderActions(order) {
        if (order.status === 'Created') {
            return `
                <button class="btn-accept" data-order-id="${order.id}">Accept Order</button>
                <button class="btn-reject" data-order-id="${order.id}">Reject</button>
            `;
        }
        
        return '';
    }

    // Open order details modal
    function openOrderDetails(order) {
        selectedOrderId = order.id;
        
        // Format order details in the modal
        orderDetailContent.innerHTML = `
            <div class="order-detail-section">
                <h3>Order Information</h3>
                <p><strong>Order ID:</strong> #${order.id}</p>
                <p><strong>Date:</strong> ${new Date(order.created_at).toLocaleString()}</p>
                <p><strong>Status:</strong> <span class="order-status status-${order.status.toLowerCase()}">${formatStatus(order.status)}</span></p>
                <p><strong>Payment Status:</strong> ${order.is_paid ? '<span style="color: #4caf50">Paid</span>' : '<span style="color: #f44336">Unpaid</span>'}</p>
                <p><strong>Payment Method:</strong> ${order.payment_method}</p>
            </div>

            <div class="order-detail-section">
                <h3>Customer Information</h3>
                <p><strong>Name:</strong> ${order.customer.username}</p>
                <p><strong>Phone:</strong> ${order.customer.phone}</p>
                <p><strong>Delivery Address:</strong> ${order.delivery_address}</p>
            </div>

            <div class="order-detail-section">
                <h3>Order Items</h3>
                <ul class="order-items-list">
                    ${generateOrderItemsList(order.items)}
                </ul>
            </div>

            <div class="order-summary">
                <div>
                    <div class="summary-line">
                        <span>Subtotal:</span>
                        <span>$${parseFloat(order.total_price).toFixed(2)}</span>
                    </div>
                    <div class="summary-line">
                        <span>Delivery Fee:</span>
                        <span>$${parseFloat(order.delivery_fee).toFixed(2)}</span>
                    </div>
                    <div class="summary-line total-line">
                        <span class="order-summary-label">Total:</span>
                        <span class="order-summary-value">$${parseFloat(order.grand_total).toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `;
        
        // Show/hide action buttons based on order status
        if (order.status === 'Created') {
            acceptOrderBtn.style.display = 'block';
            rejectOrderBtn.style.display = 'block';
        } else {
            acceptOrderBtn.style.display = 'none';
            rejectOrderBtn.style.display = 'none';
        }
        
        // Show the modal
        modal.style.display = 'block';
    }

    // Generate HTML for order items list
    function generateOrderItemsList(items) {
        if (!items || items.length === 0) {
            return '<li>No items found.</li>';
        }
        
        return items.map(item => `
            <li class="order-item">
                <div class="order-item-details">
                    <span>
                        <span class="item-quantity">${item.quantity}x</span>
                        ${item.menu_item.name}
                    </span>
                    <span class="item-price">$${parseFloat(item.unit_price * item.quantity).toFixed(2)}</span>
                </div>
                ${item.special_instructions ? `<div class="item-instructions">Note: ${item.special_instructions}</div>` : ''}
            </li>
        `).join('');
    }

    // Accept an order
    function acceptOrder(orderId) {
        // In demo mode, just update the local data
        const orderIndex = orders.findIndex(order => order.id.toString() === orderId.toString());
        
        if (orderIndex !== -1) {
            // Update order status
            orders[orderIndex].status = 'Accepted';
            
            // Update UI
            updateStats();
            displayOrders();
            
            // Close modal if open
            modal.style.display = 'none';
            
            // Show success message
            showToast('Order #' + orderId + ' accepted successfully!');
        }
    }

    // Simulate refreshing orders with 30% new orders
    function simulateRefresh() {
        showToast('Refreshing orders...');
        
        // Keep existing orders that aren't "Finish" status
        const existingOrders = orders.filter(order => order.status !== 'Finish');
        
        // Generate some new orders (30% chance of new orders)
        const newOrderCount = Math.floor(Math.random() * 3); // 0-2 new orders
        const newOrders = generateFakeOrders(newOrderCount);
        
        // Combine orders
        orders = [...existingOrders, ...newOrders];
        
        // Update UI
        updateStats();
        displayOrders();
        
        showToast(newOrderCount > 0 
            ? `Refreshed orders! ${newOrderCount} new order${newOrderCount !== 1 ? 's' : ''} received.` 
            : 'Refreshed orders! No new orders.');
    }

    // Show toast notification
    function showToast(message) {
        toastMessage.textContent = message;
        toast.className = 'toast-notification show';
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.className = toast.className.replace('show', '');
        }, 3000);
    }

    // Event Listeners
    refreshButton.addEventListener('click', simulateRefresh);
    
    // Tab buttons for filtering orders
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Update active tab
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Set filter and refresh display
            currentFilter = button.dataset.status;
            displayOrders();
        });
    });
    
    // Modal events
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    // Close modal when clicking outside of it
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Accept order button in modal
    acceptOrderBtn.addEventListener('click', () => {
        if (selectedOrderId) {
            acceptOrder(selectedOrderId);
        }
    });
    
    // Reject order button in modal
    rejectOrderBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        showToast('Order rejection feature is coming soon.');
    });

    // Initialize the dashboard with fake data
    initializeDashboard();
});