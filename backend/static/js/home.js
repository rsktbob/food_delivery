// Sample restaurant data
const recommendedRestaurants = [
    {
        id: 1,
        name: "Burger Heaven",
        image: "https://via.placeholder.com/300x200",
        cuisine: "American",
        rating: 4.7,
        reviews: 243,
        deliveryTime: "25-35 min",
        tags: ["Burgers", "Fast Food", "Family Friendly"]
    },
    {
        id: 2,
        name: "Pizza Palace",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Italian",
        rating: 4.5,
        reviews: 189,
        deliveryTime: "30-40 min",
        tags: ["Pizza", "Pasta", "Italian"]
    },
    {
        id: 3,
        name: "Sushi Supreme",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Japanese",
        rating: 4.8,
        reviews: 312,
        deliveryTime: "35-45 min",
        tags: ["Sushi", "Japanese", "Healthy"]
    },
    {
        id: 4,
        name: "Taco Fiesta",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Mexican",
        rating: 4.4,
        reviews: 156,
        deliveryTime: "20-30 min",
        tags: ["Mexican", "Tacos", "Spicy"]
    },
    {
        id: 5,
        name: "Curry House",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Indian",
        rating: 4.6,
        reviews: 205,
        deliveryTime: "35-50 min",
        tags: ["Indian", "Curry", "Vegetarian Options"]
    },
    {
        id: 6,
        name: "Mediterranean Delights",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Mediterranean",
        rating: 4.5,
        reviews: 178,
        deliveryTime: "30-45 min",
        tags: ["Mediterranean", "Healthy", "Kebabs"]
    },
    {
        id: 7,
        name: "Noodle Express",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Chinese",
        rating: 4.3,
        reviews: 167,
        deliveryTime: "25-35 min",
        tags: ["Chinese", "Noodles", "Quick Service"]
    },
    {
        id: 8,
        name: "Veggie Paradise",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Vegetarian",
        rating: 4.6,
        reviews: 198,
        deliveryTime: "25-40 min",
        tags: ["Vegetarian", "Vegan Options", "Healthy"]
    },
    {
        id: 9,
        name: "Breakfast All Day",
        image: "https://via.placeholder.com/300x200",
        cuisine: "Breakfast",
        rating: 4.5,
        reviews: 134,
        deliveryTime: "20-30 min",
        tags: ["Breakfast", "Brunch", "Coffee"]
    }
];

// Function to render star ratings
function renderStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
    
    let starsHTML = '';
    
    // Full stars
    for (let i = 0; i < fullStars; i++) {
        starsHTML += '<i class="fas fa-star"></i>';
    }
    
    // Half star if needed
    if (halfStar) {
        starsHTML += '<i class="fas fa-star-half-alt"></i>';
    }
    
    // Empty stars
    for (let i = 0; i < emptyStars; i++) {
        starsHTML += '<i class="far fa-star"></i>';
    }
    
    return starsHTML;
}

// Function to handle restaurant click
function handleRestaurantClick(restaurantId) {
    // In a real app, this would navigate to a restaurant detail page
    // For demo purposes, we'll just alert the restaurant ID
    alert(`Navigating to restaurant details page for ID: ${restaurantId}`);
    
    // In production, you might use something like:
    // window.location.href = `/restaurant-detail/${restaurantId}`;
}

// Function to chunk array into groups
function chunkArray(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

// Function to render restaurant rows
function renderRestaurants() {
    const restaurantsContainer = document.getElementById('restaurants-container');
    const restaurantRows = chunkArray(recommendedRestaurants, 3);
    
    // Clear existing content
    restaurantsContainer.innerHTML = '';
    
    // Create restaurant rows and append to container
    restaurantRows.forEach((row, rowIndex) => {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'restaurant-row';
        rowDiv.setAttribute('data-row', rowIndex);
        
        // Create restaurant cards for each restaurant in the row
        row.forEach(restaurant => {
            const colDiv = document.createElement('div');
            colDiv.className = 'restaurant-column';
            
            // Create tags HTML
            const tagsHTML = restaurant.tags.map(tag => 
                `<span class="tag">${tag}</span>`
            ).join('');
            
            // Create restaurant card HTML
            colDiv.innerHTML = `
                <div class="restaurant-card" data-id="${restaurant.id}">
                    <div class="restaurant-image">
                        <img src="${restaurant.image}" alt="${restaurant.name}" />
                        <span class="delivery-time">${restaurant.deliveryTime}</span>
                    </div>
                    <div class="restaurant-info">
                        <h3 class="restaurant-name">${restaurant.name}</h3>
                        <p class="restaurant-cuisine">${restaurant.cuisine}</p>
                        <div class="restaurant-rating">
                            <div class="stars">
                                ${renderStars(restaurant.rating)}
                            </div>
                            <span class="rating-number">${restaurant.rating}</span>
                            <span class="reviews-count">(${restaurant.reviews})</span>
                        </div>
                        <div class="restaurant-tags">
                            ${tagsHTML}
                        </div>
                    </div>
                </div>
            `;
            
            rowDiv.appendChild(colDiv);
        });
        
        restaurantsContainer.appendChild(rowDiv);
    });
    
    // Add click event listeners to restaurant cards
    document.querySelectorAll('.restaurant-card').forEach(card => {
        card.addEventListener('click', () => {
            const restaurantId = card.getAttribute('data-id');
            handleRestaurantClick(restaurantId);
        });
    });
}

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Render restaurants
    renderRestaurants();
    
    // Add event listener for search button
    const searchButton = document.querySelector('.search-button');
    searchButton.addEventListener('click', () => {
        const searchInput = document.querySelector('.search-input');
        if (searchInput.value.trim()) {
            alert(`Searching for: ${searchInput.value}`);
        }
    });
    
    // Add event listeners for category items
    document.querySelectorAll('.category-item').forEach(category => {
        category.addEventListener('click', () => {
            const categoryName = category.querySelector('span').textContent;
            alert(`Category selected: ${categoryName}`);
        });
    });
    
    // Add event listeners for "Order Now" buttons
    document.querySelectorAll('.order-now-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            // Prevent event bubbling
            e.stopPropagation();
            
            // Get offer title
            const offerTitle = button.parentElement.querySelector('h3').textContent;
            alert(`Order now clicked for offer: ${offerTitle}`);
        });
    });
    
    // Add event listeners for "View All" links
    document.querySelectorAll('.view-all').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionTitle = e.target.parentElement.querySelector('h2').textContent;
            alert(`View all clicked for: ${sectionTitle}`);
        });
    });
});