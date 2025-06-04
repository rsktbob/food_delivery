import { BrowserRouter, Routes, Route, NavLink  } from "react-router-dom";
import HeaderBar from '../components/HeaderBar';
import CustomerHomePage from '../pages/customer/CustomerHomePage';
import TestPage from '../pages/TestPage';
import RestaurantDetailPage from "../pages/customer/RestaurantDetailPage";
import CartPage from "../pages/customer/CartPage";
import OrderForm from "../pages/customer/OrderForm";
import TrackOrder from "../pages/customer/TrackOrder";


function CustomerRouter({user, handleLogout}) {
  return (
    <div className="app-container">
      <HeaderBar user={user} handleLogout={handleLogout}>
        <nav>
          <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""}>首頁</NavLink>
          <NavLink to={`/cart`} className={({ isActive }) => isActive ? "active" : ""}>
            <i className="bi bi-cart-plus-fill me-1"></i>
          </NavLink>
        </nav>
      </HeaderBar>
      
      <main>
        <Routes>
          <Route path="/" element={<CustomerHomePage user={user} />} />
          <Route path="/restaurants/:id" element={<RestaurantDetailPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/order" element={<OrderForm user={user} />} />
          <Route path="/map" element={<TrackOrder user={user} />} />
        </Routes>
      </main>
    </div>
  );
}

export default CustomerRouter;